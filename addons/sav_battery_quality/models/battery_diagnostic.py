from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


DIAGNOSTIC_SEVERITY_SELECTION = [
    ("minor", "Mineur"),
    ("major", "Majeur"),
    ("critical", "Critique"),
]

DIAGNOSTIC_STATE_SELECTION = [
    ("open", "Ouvert"),
    ("in_progress", "En traitement"),
    ("resolved", "Résolu"),
    ("rejected", "Rejeté"),
    ("closed", "Clôturé"),
]

DIAGNOSTIC_CAUSE_SELECTION = [
    ("measurement_out_of_range", "Mesure hors seuil"),
    ("visual_defect", "Défaut visuel"),
    ("assembly_issue", "Assemblage non conforme"),
    ("insulation_issue", "Isolement non conforme"),
    ("bms_issue", "BMS non conforme"),
    ("charge_discharge_issue", "Test charge/décharge non conforme"),
    ("documentation_issue", "Notice / documentation non conforme"),
    ("other", "Autre"),
]


class SavBatteryDiagnostic(models.Model):
    _name = "sav.battery.diagnostic"
    _description = "Diagnostic batterie / non-conformité"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "severity desc, date_opened desc, id desc"

    name = fields.Char(string="Référence", default="Nouveau", readonly=True, copy=False, tracking=True)
    repair_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", required=True, ondelete="cascade", tracking=True)
    checklist_id = fields.Many2one("sav.battery.checklist", string="Checklist", ondelete="set null", tracking=True)
    checklist_line_id = fields.Many2one("sav.battery.checklist.line", string="Contrôle non conforme", ondelete="set null", tracking=True)
    test_session_id = fields.Many2one("sav.battery.test.session", string="Session de test", ondelete="set null", tracking=True)
    test_measurement_id = fields.Many2one("sav.battery.test.measurement", string="Mesure non conforme", ondelete="set null", tracking=True)
    severity = fields.Selection(DIAGNOSTIC_SEVERITY_SELECTION, string="Gravité", default="major", required=True, tracking=True)
    cause = fields.Selection(DIAGNOSTIC_CAUSE_SELECTION, string="Cause probable", default="other", required=True, tracking=True)
    description = fields.Text(string="Description", required=True, tracking=True)
    corrective_action = fields.Text(string="Action corrective")
    responsible_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user, tracking=True)
    state = fields.Selection(DIAGNOSTIC_STATE_SELECTION, string="État", default="open", required=True, tracking=True)
    photo_ids = fields.Many2many("ir.attachment", string="Photos / preuves")
    date_opened = fields.Datetime(string="Date ouverture", default=fields.Datetime.now, readonly=True, tracking=True)
    date_closed = fields.Datetime(string="Date clôture", readonly=True, tracking=True)
    resolution_note = fields.Text(string="Note de résolution")

    checklist_line_phase = fields.Selection(related="checklist_line_id.phase", string="Phase", store=True, readonly=True)
    checklist_line_verdict = fields.Selection(related="checklist_line_id.verdict", string="Verdict contrôle", store=True, readonly=True)
    is_open = fields.Boolean(string="Ouvert", compute="_compute_is_open", store=True)
    is_critical_open = fields.Boolean(string="Critique ouvert", compute="_compute_is_open", store=True)

    @api.depends("state", "severity")
    def _compute_is_open(self):
        for diagnostic in self:
            diagnostic.is_open = diagnostic.state in ("open", "in_progress")
            diagnostic.is_critical_open = diagnostic.severity == "critical" and diagnostic.state in ("open", "in_progress")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                repair = self.env["sav.magasin.order"].browse(vals.get("repair_id")) if vals.get("repair_id") else False
                prefix = repair.name if repair and repair.exists() else "DIAG-BAT"
                vals["name"] = _("%s / NC-%s") % (prefix, fields.Datetime.now().strftime("%H%M%S"))
        diagnostics = super().create(vals_list)
        for diagnostic in diagnostics:
            diagnostic.message_post(body=_("Diagnostic batterie créé."))
        return diagnostics

    @api.model
    def _cause_from_checklist_line(self, line):
        phase = line.phase
        if line.measurement_type == "numeric" or line.is_out_of_range:
            return "measurement_out_of_range"
        if phase in ("diagnosis", "cell_preparation"):
            return "visual_defect"
        if phase == "assembly":
            return "assembly_issue"
        if phase == "welding":
            return "insulation_issue"
        if phase == "bms":
            return "bms_issue"
        if phase in ("charge", "discharge"):
            return "charge_discharge_issue"
        if phase == "final_validation":
            return "documentation_issue"
        return "other"

    @api.model
    def get_or_create_from_checklist_line(self, line):
        if not line or not line.exists() or line.verdict != "fail":
            return self.browse()
        existing = self.search([
            ("checklist_line_id", "=", line.id),
            ("state", "in", ["open", "in_progress", "resolved", "rejected"]),
        ], limit=1)
        measured = ""
        if line.measurement_type == "numeric" and line.is_measurement_entered:
            measured = _("\nValeur mesurée : %(value)s %(unit)s") % {"value": line.measured_value, "unit": line.unit or ""}
        elif line.measurement_type == "text" and line.measured_text:
            measured = _("\nValeur / référence : %s") % line.measured_text
        description = _(
            "Contrôle non conforme : %(control)s\nCritère attendu : %(criteria)s%(measured)s\nCommentaire technicien : %(comment)s"
        ) % {
            "control": line.name,
            "criteria": line.expected_criteria or "-",
            "measured": measured,
            "comment": line.comment or "-",
        }
        values = {
            "repair_id": line.repair_id.id,
            "checklist_id": line.checklist_id.id,
            "checklist_line_id": line.id,
            "severity": "critical" if line.blocking else "major",
            "cause": self._cause_from_checklist_line(line),
            "description": description,
            "responsible_id": line.checklist_id.quality_responsible_id.id or line.checklist_id.operator_id.id or self.env.user.id,
            "photo_ids": [(6, 0, line.proof_attachment_ids.ids)],
        }
        if existing:
            # Keep the workflow state chosen by the user, but refresh the technical content and proofs.
            existing.write({k: v for k, v in values.items() if k not in ("repair_id", "checklist_id", "checklist_line_id")})
            return existing
        return self.create(values)

    @api.model
    def get_or_create_from_test_measurement(self, measurement):
        if not measurement or not measurement.exists() or measurement.result != "fail":
            return self.browse()
        existing = self.search([
            ("test_measurement_id", "=", measurement.id),
            ("state", "in", ["open", "in_progress", "resolved", "rejected"]),
        ], limit=1)
        description = _(
            "Mesure technique non conforme : %(point)s\n"
            "Session : %(session)s\n"
            "Motif : %(reason)s\n"
            "Tension départ : %(voltage_start)s V\n"
            "Tension fin : %(voltage_end)s V\n"
            "Courant : %(current)s A\n"
            "Capacité : %(capacity)s Ah\n"
            "Température BMS : %(temperature)s °C\n"
            "Delta cellules : %(delta)s V\n"
            "Commentaire : %(comment)s"
        ) % {
            "point": measurement.name or "Mesure",
            "session": measurement.session_id.name,
            "reason": measurement.out_of_range_reason or "Hors tolérance",
            "voltage_start": measurement.voltage_start,
            "voltage_end": measurement.voltage_end,
            "current": measurement.current_a,
            "capacity": measurement.capacity_ah,
            "temperature": measurement.temperature_c,
            "delta": measurement.cell_delta_v,
            "comment": measurement.comment or "-",
        }
        severity = "critical" if (
            measurement.temperature_c >= measurement.max_temperature_c
            or measurement.voltage_end >= measurement.max_voltage_limit
            or measurement.voltage_start >= measurement.max_voltage_limit
        ) else "major"
        values = {
            "repair_id": measurement.repair_id.id,
            "checklist_id": measurement.checklist_id.id if measurement.checklist_id else False,
            "test_session_id": measurement.session_id.id,
            "test_measurement_id": measurement.id,
            "severity": severity,
            "cause": "charge_discharge_issue",
            "description": description,
            "responsible_id": measurement.session_id.operator_id.id or self.env.user.id,
            "photo_ids": [(6, 0, measurement.attachment_ids.ids)],
        }
        if existing:
            existing.write({k: v for k, v in values.items() if k not in ("repair_id", "test_session_id", "test_measurement_id")})
            return existing
        return self.create(values)

    def action_start(self):
        self.write({"state": "in_progress"})
        return True

    def action_resolve(self):
        for diagnostic in self:
            if not diagnostic.corrective_action:
                raise ValidationError(_("Une action corrective est obligatoire pour résoudre un diagnostic."))
        self.write({"state": "resolved", "date_closed": fields.Datetime.now()})
        return True

    def action_reject(self):
        for diagnostic in self:
            if not diagnostic.resolution_note and not diagnostic.corrective_action:
                raise ValidationError(_("Une justification est obligatoire pour rejeter un diagnostic."))
        self.write({"state": "rejected", "date_closed": fields.Datetime.now()})
        return True

    def action_close(self):
        for diagnostic in self:
            if diagnostic.state not in ("resolved", "rejected"):
                raise ValidationError(_("Seuls les diagnostics résolus ou rejetés peuvent être clôturés."))
        self.write({"state": "closed", "date_closed": fields.Datetime.now()})
        return True

    def action_reopen(self):
        self.write({"state": "open", "date_closed": False})
        return True
