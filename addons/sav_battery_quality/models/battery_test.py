from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


TEST_TYPE_SELECTION = [
    ("charge", "Charge"),
    ("discharge", "Décharge"),
    ("bms", "BMS"),
    ("capacity", "Capacité"),
    ("balancing", "Équilibrage"),
]

TEST_STATE_SELECTION = [
    ("draft", "Brouillon"),
    ("running", "En cours"),
    ("done", "Terminé"),
    ("validated", "Validé"),
    ("cancelled", "Annulé"),
]

TEST_RESULT_SELECTION = [
    ("pending", "En attente"),
    ("pass", "Conforme"),
    ("fail", "Non conforme"),
]


class SavBatteryTestSession(models.Model):
    _name = "sav.battery.test.session"
    _description = "Session de test batterie"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_datetime desc, id desc"

    name = fields.Char(string="Référence", default="Nouveau", readonly=True, copy=False, tracking=True)
    repair_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", required=True, ondelete="cascade", tracking=True)
    checklist_id = fields.Many2one("sav.battery.checklist", string="Checklist liée", ondelete="set null", tracking=True)
    test_type = fields.Selection(TEST_TYPE_SELECTION, string="Type de test", required=True, default="charge", tracking=True)
    start_datetime = fields.Datetime(string="Début", tracking=True)
    end_datetime = fields.Datetime(string="Fin", tracking=True)
    duration = fields.Float(string="Durée (h)", compute="_compute_duration", store=True)
    operator_id = fields.Many2one("res.users", string="Opérateur", default=lambda self: self.env.user, tracking=True)
    state = fields.Selection(TEST_STATE_SELECTION, string="État", default="draft", required=True, tracking=True)
    result = fields.Selection(TEST_RESULT_SELECTION, string="Résultat", default="pending", required=True, tracking=True, compute="_compute_result", store=True, readonly=False)
    attachment_ids = fields.Many2many("ir.attachment", string="Fichiers de mesure")
    measurement_ids = fields.One2many("sav.battery.test.measurement", "session_id", string="Mesures")
    note = fields.Text(string="Commentaire session")

    measurement_count = fields.Integer(string="Nombre de mesures", compute="_compute_measurement_summary", store=True)
    fail_measurement_count = fields.Integer(string="Mesures non conformes", compute="_compute_measurement_summary", store=True)
    voltage_start = fields.Float(string="Tension départ (V)", compute="_compute_measurement_summary", store=True)
    voltage_end = fields.Float(string="Tension fin (V)", compute="_compute_measurement_summary", store=True)
    current_a = fields.Float(string="Courant max (A)", compute="_compute_measurement_summary", store=True)
    capacity_ah = fields.Float(string="Capacité mesurée (Ah)", compute="_compute_measurement_summary", store=True)
    temperature_max = fields.Float(string="Température max (°C)", compute="_compute_measurement_summary", store=True)
    cell_delta_v = fields.Float(string="Delta cellules max (V)", compute="_compute_measurement_summary", store=True)
    validation_message = fields.Text(string="Blocages validation", compute="_compute_validation_message", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                repair = self.env["sav.magasin.order"].browse(vals.get("repair_id")) if vals.get("repair_id") else False
                prefix = repair.name if repair and repair.exists() else "TEST-BAT"
                test_type = vals.get("test_type") or "test"
                vals["name"] = _("%s / TEST-%s-%s") % (prefix, test_type.upper(), fields.Datetime.now().strftime("%H%M%S"))
        return super().create(vals_list)

    @api.depends("start_datetime", "end_datetime")
    def _compute_duration(self):
        for session in self:
            if session.start_datetime and session.end_datetime and session.end_datetime >= session.start_datetime:
                delta = session.end_datetime - session.start_datetime
                session.duration = delta.total_seconds() / 3600.0
            else:
                session.duration = 0.0

    @api.depends(
        "measurement_ids.result",
        "measurement_ids.voltage_start",
        "measurement_ids.voltage_end",
        "measurement_ids.current_a",
        "measurement_ids.capacity_ah",
        "measurement_ids.temperature_c",
        "measurement_ids.cell_delta_v",
    )
    def _compute_measurement_summary(self):
        for session in self:
            measurements = session.measurement_ids
            session.measurement_count = len(measurements)
            session.fail_measurement_count = len(measurements.filtered(lambda m: m.result == "fail"))
            ordered = measurements.sorted(lambda m: (m.sequence, m.id))
            session.voltage_start = ordered[0].voltage_start if ordered else 0.0
            session.voltage_end = ordered[-1].voltage_end if ordered else 0.0
            session.current_a = max(measurements.mapped("current_a") or [0.0])
            session.capacity_ah = max(measurements.mapped("capacity_ah") or [0.0])
            session.temperature_max = max(measurements.mapped("temperature_c") or [0.0])
            session.cell_delta_v = max(measurements.mapped("cell_delta_v") or [0.0])

    @api.depends("measurement_count", "fail_measurement_count", "state")
    def _compute_result(self):
        for session in self:
            if session.state == "cancelled":
                session.result = "pending"
            elif not session.measurement_count:
                session.result = "pending"
            elif session.fail_measurement_count:
                session.result = "fail"
            else:
                session.result = "pass"

    @api.depends("state", "measurement_count", "fail_measurement_count", "note")
    def _compute_validation_message(self):
        for session in self:
            messages = []
            if not session.measurement_count:
                messages.append(_("Aucune mesure n'est rattachée à cette session."))
            if session.fail_measurement_count and not session.note:
                messages.append(_("Un commentaire session est requis si une mesure est non conforme."))
            session.validation_message = "\n".join(messages)

    def action_start(self):
        self.write({"state": "running", "start_datetime": fields.Datetime.now()})
        return True

    def action_done(self):
        for session in self:
            if not session.start_datetime:
                session.start_datetime = fields.Datetime.now()
            session.end_datetime = fields.Datetime.now()
            session.state = "done"
        return True

    def action_validate(self):
        Diagnostic = self.env["sav.battery.diagnostic"]
        for session in self:
            if not session.measurement_count:
                raise ValidationError(_("Impossible de valider : aucune mesure n'est saisie."))
            if session.fail_measurement_count and not session.note:
                raise ValidationError(_("Un commentaire est obligatoire avant validation d'une session non conforme."))
            for measurement in session.measurement_ids.filtered(lambda m: m.result == "fail"):
                Diagnostic.get_or_create_from_test_measurement(measurement)
            session.write({"state": "validated"})
            session.message_post(body=_("Session de test batterie validée."))
        return True

    def action_cancel(self):
        self.write({"state": "cancelled"})
        return True

    def action_reopen(self):
        self.write({"state": "draft"})
        return True


class SavBatteryTestMeasurement(models.Model):
    _name = "sav.battery.test.measurement"
    _description = "Mesure technique batterie"
    _order = "session_id, sequence, id"

    session_id = fields.Many2one("sav.battery.test.session", string="Session", required=True, ondelete="cascade")
    repair_id = fields.Many2one(related="session_id.repair_id", string="Dossier batterie", store=True, readonly=True)
    checklist_id = fields.Many2one(related="session_id.checklist_id", string="Checklist", store=True, readonly=True)
    sequence = fields.Integer(default=10)
    measured_at = fields.Datetime(string="Horodatage", default=fields.Datetime.now)
    name = fields.Char(string="Point de mesure", default="Mesure")
    voltage_start = fields.Float(string="Tension départ (V)")
    voltage_end = fields.Float(string="Tension fin (V)")
    current_a = fields.Float(string="Courant (A)")
    capacity_ah = fields.Float(string="Capacité (Ah)")
    temperature_c = fields.Float(string="Température BMS (°C)")
    cell_delta_v = fields.Float(string="Delta cellules (V)")
    unit = fields.Char(string="Unité principale")
    result = fields.Selection(TEST_RESULT_SELECTION, string="Résultat", compute="_compute_result", store=True, readonly=False)
    comment = fields.Text(string="Commentaire")
    attachment_ids = fields.Many2many("ir.attachment", string="Preuves / fichiers")

    max_voltage_limit = fields.Float(string="Seuil tension max (V)", default=59.99)
    max_temperature_c = fields.Float(string="Seuil température max (°C)", default=59.99)
    max_cell_delta_v = fields.Float(string="Seuil delta max (V)", default=0.05)
    min_capacity_ah = fields.Float(string="Capacité minimale (Ah)")

    out_of_range_reason = fields.Char(string="Motif hors seuil", compute="_compute_result", store=True)

    @api.onchange("session_id")
    def _onchange_session_id(self):
        for measurement in self:
            repair = measurement.session_id.repair_id
            if repair and repair.battery_capacity_ah and not measurement.min_capacity_ah:
                measurement.min_capacity_ah = repair.battery_capacity_ah * 0.8

    @api.depends(
        "voltage_start", "voltage_end", "temperature_c", "cell_delta_v", "capacity_ah",
        "max_voltage_limit", "max_temperature_c", "max_cell_delta_v", "min_capacity_ah",
    )
    def _compute_result(self):
        for measurement in self:
            reasons = []
            if measurement.voltage_start and measurement.voltage_start >= measurement.max_voltage_limit:
                reasons.append(_("Tension départ >= %(limit)s V") % {"limit": measurement.max_voltage_limit})
            if measurement.voltage_end and measurement.voltage_end >= measurement.max_voltage_limit:
                reasons.append(_("Tension fin >= %(limit)s V") % {"limit": measurement.max_voltage_limit})
            if measurement.temperature_c and measurement.temperature_c >= measurement.max_temperature_c:
                reasons.append(_("Température BMS >= %(limit)s °C") % {"limit": measurement.max_temperature_c})
            if measurement.cell_delta_v and measurement.cell_delta_v > measurement.max_cell_delta_v:
                reasons.append(_("Delta cellules > %(limit)s V") % {"limit": measurement.max_cell_delta_v})
            if measurement.min_capacity_ah and measurement.capacity_ah and measurement.capacity_ah < measurement.min_capacity_ah:
                reasons.append(_("Capacité mesurée < %(limit)s Ah") % {"limit": measurement.min_capacity_ah})
            has_any_value = any([
                measurement.voltage_start,
                measurement.voltage_end,
                measurement.current_a,
                measurement.capacity_ah,
                measurement.temperature_c,
                measurement.cell_delta_v,
            ])
            measurement.out_of_range_reason = "; ".join(reasons)
            if reasons:
                measurement.result = "fail"
            elif has_any_value:
                measurement.result = "pass"
            else:
                measurement.result = "pending"
