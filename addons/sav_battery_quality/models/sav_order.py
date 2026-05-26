from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


BATTERY_STAGE_SELECTION = [
    ("draft", "Brouillon"),
    ("received", "Batterie reçue"),
    ("quarantine", "Quarantaine"),
    ("diagnosis", "Diagnostic batterie"),
    ("waiting_customer_validation", "Attente validation client"),
    ("repair_in_progress", "Réparation en cours"),
    ("assembly", "Assemblage pack"),
    ("testing", "Tests charge/décharge"),
    ("quality_check", "Contrôle qualité"),
    ("validated", "Validée"),
    ("delivered", "Livrée"),
    ("blocked", "Bloquée"),
    ("cancelled", "Annulée"),
]


class SavMagasinOrderBattery(models.Model):
    _inherit = "sav.magasin.order"

    state = fields.Selection(
        selection_add=[
            ("received", "Batterie reçue"),
            ("quarantine", "Quarantaine"),
            ("assembly", "Assemblage pack"),
            ("testing", "Tests charge/décharge"),
            ("quality_check", "Contrôle qualité"),
            ("validated", "Validée"),
            ("delivered", "Livrée"),
            ("blocked", "Bloquée"),
        ],
        ondelete={
            "received": "set default",
            "quarantine": "set default",
            "assembly": "set default",
            "testing": "set default",
            "quality_check": "set default",
            "validated": "set default",
            "delivered": "set default",
            "blocked": "set default",
        },
    )

    is_battery_repair = fields.Boolean(string="Dossier batterie", default=True, tracking=True)
    battery_model_id = fields.Many2one("sav.battery.model", string="Modèle batterie")
    battery_serial = fields.Char(string="Numéro série batterie", tracking=True)
    battery_nominal_voltage = fields.Float(string="Tension nominale (V)", tracking=True)
    battery_max_voltage = fields.Float(string="Tension maximale (V)", tracking=True)
    battery_capacity_ah = fields.Float(string="Capacité (Ah)")
    battery_chemistry = fields.Selection(
        [
            ("li_ion", "Li-ion"),
            ("lifepo4", "LiFePO4"),
            ("nimh", "NiMH"),
            ("lead", "Plomb"),
            ("other", "Autre"),
        ],
        string="Chimie",
        default="li_ion",
    )
    battery_series_count = fields.Integer(string="Cellules en série")
    battery_parallel_count = fields.Integer(string="Cellules en parallèle")
    battery_architecture = fields.Char(string="Architecture S/P", compute="_compute_battery_architecture", store=True)
    bms_type = fields.Char(string="Type de BMS")
    connector_type = fields.Char(string="Connectique")
    charger_voltage = fields.Float(string="Tension chargeur (V)")
    is_under_60v = fields.Boolean(string="Compatible < 60 V", compute="_compute_is_under_60v", store=True)
    battery_stage = fields.Selection(BATTERY_STAGE_SELECTION, string="Étape batterie", default="draft", tracking=True)
    battery_blocking_reason = fields.Char(string="Blocage batterie", compute="_compute_battery_blocking_reason", store=True)
    battery_notice_version = fields.Char(string="Version notice")
    battery_quality_responsible_id = fields.Many2one("res.users", string="Responsable qualité")
    battery_checklist_ids = fields.One2many("sav.battery.checklist", "repair_id", string="Checklists batterie")
    battery_checklist_count = fields.Integer(string="Checklists batterie", compute="_compute_battery_checklist_count")
    has_validated_battery_checklist = fields.Boolean(string="Checklist validée disponible", compute="_compute_battery_checklist_count", store=True)
    battery_open_blocking_fail_count = fields.Integer(string="Non-conformités bloquantes checklist", compute="_compute_battery_checklist_count", store=True)
    battery_diagnostic_ids = fields.One2many("sav.battery.diagnostic", "repair_id", string="Diagnostics batterie")
    battery_diagnostic_count = fields.Integer(string="Diagnostics batterie", compute="_compute_battery_diagnostic_count")
    battery_open_diagnostic_count = fields.Integer(string="Diagnostics ouverts", compute="_compute_battery_diagnostic_count", store=True)
    battery_open_critical_diagnostic_count = fields.Integer(string="Diagnostics critiques ouverts", compute="_compute_battery_diagnostic_count", store=True)
    battery_test_session_ids = fields.One2many("sav.battery.test.session", "repair_id", string="Tests batterie")
    battery_test_session_count = fields.Integer(string="Tests batterie", compute="_compute_battery_test_session_count")
    battery_validated_test_count = fields.Integer(string="Tests validés", compute="_compute_battery_test_session_count", store=True)
    battery_failed_test_count = fields.Integer(string="Tests non conformes", compute="_compute_battery_test_session_count", store=True)
    battery_last_test_result = fields.Selection([
        ("pending", "En attente"),
        ("pass", "Conforme"),
        ("fail", "Non conforme"),
    ], string="Dernier résultat test", compute="_compute_battery_test_session_count", store=True)

    @api.depends("battery_series_count", "battery_parallel_count")
    def _compute_battery_architecture(self):
        for order in self:
            if order.battery_series_count and order.battery_parallel_count:
                order.battery_architecture = "%sS%sP" % (order.battery_series_count, order.battery_parallel_count)
            elif order.battery_series_count:
                order.battery_architecture = "%sS" % order.battery_series_count
            else:
                order.battery_architecture = False

    @api.depends("is_battery_repair", "battery_max_voltage")
    def _compute_is_under_60v(self):
        for order in self:
            order.is_under_60v = bool(order.is_battery_repair and order.battery_max_voltage and order.battery_max_voltage < 60.0)

    @api.depends("is_battery_repair", "battery_nominal_voltage", "battery_max_voltage", "is_under_60v")
    def _compute_battery_blocking_reason(self):
        for order in self:
            reason = False
            if order.is_battery_repair:
                if not order.battery_nominal_voltage:
                    reason = _("Tension nominale batterie manquante.")
                elif not order.battery_max_voltage:
                    reason = _("Tension maximale batterie manquante.")
                elif order.battery_max_voltage >= 60.0:
                    reason = _("Batterie hors périmètre : tension maximale >= 60 V.")
            order.battery_blocking_reason = reason

    @api.depends("battery_checklist_ids.state", "battery_checklist_ids.blocking_fail_count")
    def _compute_battery_checklist_count(self):
        for order in self:
            order.battery_checklist_count = len(order.battery_checklist_ids)
            order.has_validated_battery_checklist = bool(order.battery_checklist_ids.filtered(lambda c: c.state in ("validated", "locked")))
            order.battery_open_blocking_fail_count = sum(order.battery_checklist_ids.filtered(lambda c: c.state not in ("cancelled",)).mapped("blocking_fail_count"))

    @api.depends("battery_diagnostic_ids.state", "battery_diagnostic_ids.severity")
    def _compute_battery_diagnostic_count(self):
        for order in self:
            diagnostics = order.battery_diagnostic_ids
            order.battery_diagnostic_count = len(diagnostics)
            order.battery_open_diagnostic_count = len(diagnostics.filtered(lambda diagnostic: diagnostic.state in ("open", "in_progress")))
            order.battery_open_critical_diagnostic_count = len(diagnostics.filtered(lambda diagnostic: diagnostic.severity == "critical" and diagnostic.state in ("open", "in_progress")))

    @api.onchange("battery_model_id")
    def _onchange_battery_model_id(self):
        for order in self:
            model = order.battery_model_id
            if not model:
                continue
            order.battery_nominal_voltage = model.nominal_voltage
            order.battery_max_voltage = model.max_voltage
            order.battery_capacity_ah = model.capacity_ah
            order.battery_chemistry = model.chemistry
            order.battery_series_count = model.series_count
            order.battery_parallel_count = model.parallel_count
            order.bms_type = model.bms_type
            order.connector_type = model.connector_type
            order.charger_voltage = model.charger_voltage
            if not order.device_name:
                order.device_name = model.name

    @api.constrains("is_battery_repair", "battery_nominal_voltage", "battery_max_voltage", "charger_voltage")
    def _check_battery_voltage_limit(self):
        for order in self:
            if not order.is_battery_repair:
                continue
            if order.battery_nominal_voltage and order.battery_nominal_voltage >= 60.0:
                raise ValidationError(_("La tension nominale doit être strictement inférieure à 60 V."))
            if order.battery_max_voltage and order.battery_max_voltage >= 60.0:
                raise ValidationError(_("Workflow interdit : la tension maximale batterie doit être strictement inférieure à 60 V."))
            if order.charger_voltage and order.charger_voltage >= 60.0:
                raise ValidationError(_("La tension chargeur associée doit être strictement inférieure à 60 V."))

    def _get_deposit_missing_fields(self):
        missing = super()._get_deposit_missing_fields()
        self.ensure_one()
        if self.is_battery_repair:
            if not self.battery_nominal_voltage:
                missing.append(_("Tension nominale batterie"))
            if not self.battery_max_voltage:
                missing.append(_("Tension maximale batterie"))
            if not self.battery_capacity_ah:
                missing.append(_("Capacité batterie Ah"))
            if not self.battery_chemistry:
                missing.append(_("Chimie batterie"))
            if self.battery_max_voltage and self.battery_max_voltage >= 60.0:
                missing.append(_("Batterie compatible < 60 V"))
        return missing

    def action_validate_deposit(self):
        for order in self:
            if order.is_battery_repair and order.battery_max_voltage and order.battery_max_voltage >= 60.0:
                raise ValidationError(_("Impossible de valider : batterie >= 60 V. Utiliser une procédure hors périmètre."))
        res = super().action_validate_deposit()
        for order in self:
            if order.is_battery_repair:
                order.write({"battery_stage": "received"})
        return res

    def action_battery_quarantine(self):
        self.write({"state": "quarantine", "battery_stage": "quarantine"})
        self.message_post(body=_("Batterie placée en quarantaine."))
        return True

    def action_battery_assembly(self):
        self.write({"state": "assembly", "battery_stage": "assembly"})
        self.message_post(body=_("Phase assemblage batterie démarrée."))
        return True

    def action_battery_testing(self):
        self.write({"state": "testing", "battery_stage": "testing"})
        self.message_post(body=_("Tests charge/décharge démarrés."))
        return True

    def action_battery_quality_check(self):
        self.write({"state": "quality_check", "battery_stage": "quality_check"})
        self.message_post(body=_("Contrôle qualité batterie démarré."))
        return True

    def action_battery_validated(self):
        for order in self:
            if not order.has_validated_battery_checklist:
                raise ValidationError(_("Impossible de valider la batterie : aucune checklist batterie validée n’est disponible."))
            open_checklists = order.battery_checklist_ids.filtered(lambda c: c.state not in ("validated", "locked", "cancelled"))
            if open_checklists:
                raise ValidationError(_("Impossible de valider la batterie : une checklist batterie est encore ouverte."))
            if order.battery_open_blocking_fail_count:
                raise ValidationError(_("Impossible de valider la batterie : une non-conformité bloquante reste ouverte dans une checklist."))
            if order.battery_open_critical_diagnostic_count:
                raise ValidationError(_("Impossible de valider la batterie : un diagnostic critique est encore ouvert."))
            if order.battery_max_voltage >= 60.0:
                raise ValidationError(_("Impossible de valider : batterie >= 60 V."))
        self.write({"state": "validated", "battery_stage": "validated"})
        self.message_post(body=_("Batterie validée qualité."))
        return True

    def action_battery_delivered(self):
        self.write({"state": "delivered", "battery_stage": "delivered"})
        self.message_post(body=_("Batterie livrée / restituée."))
        return True

    def action_battery_blocked(self):
        self.write({"state": "blocked", "battery_stage": "blocked"})
        self.message_post(body=_("Dossier batterie bloqué."))
        return True

    def action_create_battery_checklist(self):
        self.ensure_one()
        template = self.env["sav.battery.checklist.template"].search([("active", "=", True)], order="id", limit=1)
        if not template:
            raise ValidationError(_("Aucun modèle de checklist batterie actif n’est disponible."))
        checklist = self.env["sav.battery.checklist"].create_from_template(self, template)
        return {
            "type": "ir.actions.act_window",
            "name": _("Checklist batterie"),
            "res_model": "sav.battery.checklist",
            "res_id": checklist.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_battery_checklists(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Checklists batterie"),
            "res_model": "sav.battery.checklist",
            "view_mode": "list,form",
            "domain": [("repair_id", "=", self.id)],
            "context": {"default_repair_id": self.id},
        }

    def action_open_battery_diagnostics(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Diagnostics batterie"),
            "res_model": "sav.battery.diagnostic",
            "view_mode": "list,form",
            "domain": [("repair_id", "=", self.id)],
            "context": {"default_repair_id": self.id},
        }

    def action_create_battery_test_session(self):
        self.ensure_one()
        checklist = self.battery_checklist_ids.filtered(lambda c: c.state not in ("cancelled",))[:1]
        session = self.env["sav.battery.test.session"].create({
            "repair_id": self.id,
            "checklist_id": checklist.id if checklist else False,
            "test_type": "charge" if self.battery_stage != "testing" else "discharge",
            "operator_id": self.env.user.id,
            "state": "draft",
        })
        return {
            "type": "ir.actions.act_window",
            "name": _("Session de test batterie"),
            "res_model": "sav.battery.test.session",
            "res_id": session.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_battery_test_sessions(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Tests batterie"),
            "res_model": "sav.battery.test.session",
            "view_mode": "list,form",
            "domain": [("repair_id", "=", self.id)],
            "context": {"default_repair_id": self.id},
        }

    def action_print_battery_technician_report(self):
        self.ensure_one()
        return self.env.ref("sav_battery_quality.action_report_battery_technician").report_action(self)
