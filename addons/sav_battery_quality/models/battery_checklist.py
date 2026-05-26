from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


PHASE_SELECTION = [
    ("identification", "Identification batterie"),
    ("diagnosis", "Diagnostic initial"),
    ("cell_preparation", "Préparation cellules"),
    ("assembly", "Assemblage pack"),
    ("welding", "Contrôle soudures / isolants"),
    ("bms", "Contrôle BMS"),
    ("charge", "Test charge"),
    ("discharge", "Test décharge"),
    ("final_validation", "Validation finale"),
]

MEASUREMENT_TYPE_SELECTION = [
    ("boolean", "Conformité oui/non"),
    ("numeric", "Mesure chiffrée"),
    ("text", "Texte / référence"),
    ("photo", "Preuve photo"),
]

VERDICT_SELECTION = [
    ("pending", "En attente"),
    ("pass", "Conforme"),
    ("fail", "Non conforme"),
    ("na", "Non applicable"),
]


class SavBatteryChecklistTemplate(models.Model):
    _name = "sav.battery.checklist.template"
    _description = "Modèle checklist batterie"
    _order = "name"

    name = fields.Char(required=True)
    code = fields.Char()
    version = fields.Char(default="1.0")
    active = fields.Boolean(default=True)
    description = fields.Text()
    line_ids = fields.One2many("sav.battery.checklist.template.line", "template_id", string="Contrôles")
    line_count = fields.Integer(string="Nombre de contrôles", compute="_compute_line_count")

    def _compute_line_count(self):
        for template in self:
            template.line_count = len(template.line_ids)


class SavBatteryChecklistTemplateLine(models.Model):
    _name = "sav.battery.checklist.template.line"
    _description = "Ligne modèle checklist batterie"
    _order = "template_id, sequence, id"

    template_id = fields.Many2one("sav.battery.checklist.template", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    phase = fields.Selection(PHASE_SELECTION, required=True, default="identification")
    name = fields.Char(string="Contrôle", required=True)
    expected_criteria = fields.Text(string="Critère attendu")
    measurement_type = fields.Selection(MEASUREMENT_TYPE_SELECTION, default="boolean", required=True)
    unit = fields.Char(string="Unité")
    use_min_value = fields.Boolean(string="Seuil minimum actif")
    min_value = fields.Float(string="Seuil minimum")
    use_max_value = fields.Boolean(string="Seuil maximum actif")
    max_value = fields.Float(string="Seuil maximum")
    required = fields.Boolean(string="Obligatoire", default=True)
    blocking = fields.Boolean(string="Bloquant", default=False)
    requires_photo_on_fail = fields.Boolean(string="Photo obligatoire si non conforme", default=True)
    note = fields.Text(string="Instruction atelier")


class SavBatteryChecklist(models.Model):
    _name = "sav.battery.checklist"
    _description = "Checklist qualité batterie"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(default="Nouvelle checklist", readonly=True, copy=False)
    repair_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", required=True, ondelete="cascade", tracking=True)
    template_id = fields.Many2one("sav.battery.checklist.template", string="Modèle", required=True)
    template_version = fields.Char(string="Version modèle")
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("in_progress", "En cours"),
            ("to_correct", "À corriger"),
            ("validated", "Validée"),
            ("locked", "Verrouillée"),
            ("cancelled", "Annulée"),
        ],
        default="draft",
        tracking=True,
        required=True,
    )
    operator_id = fields.Many2one("res.users", string="Technicien", default=lambda self: self.env.user)
    quality_responsible_id = fields.Many2one("res.users", string="Responsable qualité")
    start_datetime = fields.Datetime(string="Début", default=fields.Datetime.now)
    end_datetime = fields.Datetime(string="Fin")
    locked_datetime = fields.Datetime(string="Verrouillée le", readonly=True)
    line_ids = fields.One2many("sav.battery.checklist.line", "checklist_id", string="Contrôles")
    comment = fields.Text(string="Commentaire général")
    validation_message = fields.Text(string="Blocages validation", compute="_compute_validation_message", store=True)

    completion_rate = fields.Float(string="Progression (%)", compute="_compute_summary", store=True)
    required_count = fields.Integer(string="Contrôles obligatoires", compute="_compute_summary", store=True)
    completed_required_count = fields.Integer(string="Obligatoires complétés", compute="_compute_summary", store=True)
    pass_count = fields.Integer(string="Conformes", compute="_compute_summary", store=True)
    fail_count = fields.Integer(string="Non conformes", compute="_compute_summary", store=True)
    na_count = fields.Integer(string="Non applicables", compute="_compute_summary", store=True)
    pending_count = fields.Integer(string="En attente", compute="_compute_summary", store=True)
    blocking_fail_count = fields.Integer(string="Non-conformités bloquantes", compute="_compute_summary", store=True)
    critical_photo_missing_count = fields.Integer(string="Photos critiques manquantes", compute="_compute_summary", store=True)
    diagnostic_count = fields.Integer(string="Diagnostics", compute="_compute_summary", store=True)
    open_diagnostic_count = fields.Integer(string="Diagnostics ouverts", compute="_compute_summary", store=True)
    open_critical_diagnostic_count = fields.Integer(string="Diagnostics critiques ouverts", compute="_compute_summary", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("name") or vals.get("name") == "Nouvelle checklist":
                repair = self.env["sav.magasin.order"].browse(vals.get("repair_id")) if vals.get("repair_id") else False
                prefix = repair.name if repair and repair.exists() else "BAT"
                vals["name"] = _("Checklist qualité - %s") % prefix
        return super().create(vals_list)

    @api.model
    def create_from_template(self, repair, template):
        checklist = self.create({
            "repair_id": repair.id,
            "template_id": template.id,
            "template_version": template.version,
            "quality_responsible_id": repair.battery_quality_responsible_id.id if repair.battery_quality_responsible_id else False,
            "state": "in_progress",
        })
        for template_line in template.line_ids:
            self.env["sav.battery.checklist.line"].create({
                "checklist_id": checklist.id,
                "sequence": template_line.sequence,
                "phase": template_line.phase,
                "name": template_line.name,
                "expected_criteria": template_line.expected_criteria,
                "measurement_type": template_line.measurement_type,
                "unit": template_line.unit,
                "use_min_value": template_line.use_min_value,
                "min_value": template_line.min_value,
                "use_max_value": template_line.use_max_value,
                "max_value": template_line.max_value,
                "required": template_line.required,
                "blocking": template_line.blocking,
                "requires_photo_on_fail": template_line.requires_photo_on_fail,
                "instruction": template_line.note,
            })
        return checklist

    @api.depends(
        "line_ids.verdict",
        "line_ids.required",
        "line_ids.blocking",
        "line_ids.is_measurement_entered",
        "line_ids.measurement_type",
        "line_ids.proof_attachment_ids",
        "line_ids.requires_photo_on_fail",
        "line_ids.diagnostic_ids.state",
        "line_ids.diagnostic_ids.severity",
    )
    def _compute_summary(self):
        for checklist in self:
            lines = checklist.line_ids
            required_lines = lines.filtered("required")
            completed_required = required_lines.filtered(lambda line: line.is_complete)
            total_required = len(required_lines)
            checklist.required_count = total_required
            checklist.completed_required_count = len(completed_required)
            checklist.completion_rate = (len(completed_required) / total_required * 100.0) if total_required else 100.0
            checklist.pass_count = len(lines.filtered(lambda line: line.verdict == "pass"))
            checklist.fail_count = len(lines.filtered(lambda line: line.verdict == "fail"))
            checklist.na_count = len(lines.filtered(lambda line: line.verdict == "na"))
            checklist.pending_count = len(lines.filtered(lambda line: line.verdict == "pending"))
            checklist.blocking_fail_count = len(lines.filtered(lambda line: line.verdict == "fail" and line.blocking))
            checklist.critical_photo_missing_count = len(lines.filtered(lambda line: line.verdict == "fail" and line.requires_photo_on_fail and not line.proof_attachment_ids))
            diagnostics = lines.mapped("diagnostic_ids")
            checklist.diagnostic_count = len(diagnostics)
            checklist.open_diagnostic_count = len(diagnostics.filtered(lambda diagnostic: diagnostic.state in ("open", "in_progress")))
            checklist.open_critical_diagnostic_count = len(diagnostics.filtered(lambda diagnostic: diagnostic.severity == "critical" and diagnostic.state in ("open", "in_progress")))

    @api.depends(
        "line_ids.verdict",
        "line_ids.required",
        "line_ids.comment",
        "line_ids.proof_attachment_ids",
        "line_ids.requires_photo_on_fail",
        "line_ids.is_complete",
    )
    def _compute_validation_message(self):
        for checklist in self:
            messages = []
            pending_required = checklist.line_ids.filtered(lambda line: line.required and not line.is_complete)
            if pending_required:
                messages.append(_("Contrôles obligatoires incomplets : %s") % len(pending_required))
            fail_without_comment = checklist.line_ids.filtered(lambda line: line.verdict == "fail" and not line.comment)
            if fail_without_comment:
                messages.append(_("Non-conformités sans commentaire : %s") % len(fail_without_comment))
            fail_without_photo = checklist.line_ids.filtered(lambda line: line.verdict == "fail" and line.requires_photo_on_fail and not line.proof_attachment_ids)
            if fail_without_photo:
                messages.append(_("Non-conformités critiques sans preuve photo : %s") % len(fail_without_photo))
            checklist.validation_message = "\n".join(messages)

    def action_validate(self):
        for checklist in self:
            if checklist.state == "locked":
                raise ValidationError(_("Cette checklist est verrouillée."))
            pending_required = checklist.line_ids.filtered(lambda line: line.required and not line.is_complete)
            if pending_required:
                raise ValidationError(_("Validation impossible : certains contrôles obligatoires sont incomplets."))
            fail_without_comment = checklist.line_ids.filtered(lambda line: line.verdict == "fail" and not line.comment)
            if fail_without_comment:
                raise ValidationError(_("Validation impossible : chaque contrôle non conforme doit avoir un commentaire."))
            fail_without_photo = checklist.line_ids.filtered(lambda line: line.verdict == "fail" and line.requires_photo_on_fail and not line.proof_attachment_ids)
            if fail_without_photo:
                raise ValidationError(_("Validation impossible : chaque contrôle critique non conforme doit avoir une preuve photo ou pièce jointe."))
            fail_lines = checklist.line_ids.filtered(lambda line: line.verdict == "fail")
            for line in fail_lines:
                self.env["sav.battery.diagnostic"].get_or_create_from_checklist_line(line)
            checklist.write({"state": "to_correct" if fail_lines else "validated", "end_datetime": fields.Datetime.now()})
            if fail_lines:
                checklist.message_post(body=_("Checklist validée avec non-conformités : %s diagnostic(s) créé(s) ou mis à jour.") % len(fail_lines))
            else:
                checklist.message_post(body=_("Checklist batterie validée sans non-conformité."))
        return True

    def action_lock(self):
        for checklist in self:
            if checklist.state != "validated":
                raise ValidationError(_("Seule une checklist validée peut être verrouillée."))
        self.write({"state": "locked", "locked_datetime": fields.Datetime.now()})
        return True

    def action_reset_to_progress(self):
        for checklist in self:
            if checklist.state == "locked":
                raise ValidationError(_("Une checklist verrouillée ne peut pas être réouverte sans procédure de révision."))
        self.write({"state": "in_progress", "end_datetime": False})
        return True

    def action_cancel(self):
        for checklist in self:
            if checklist.state == "locked":
                raise ValidationError(_("Une checklist verrouillée ne peut pas être annulée."))
        self.write({"state": "cancelled"})
        return True


class SavBatteryChecklistLine(models.Model):
    _name = "sav.battery.checklist.line"
    _description = "Contrôle checklist batterie"
    _order = "checklist_id, sequence, id"

    checklist_id = fields.Many2one("sav.battery.checklist", required=True, ondelete="cascade")
    repair_id = fields.Many2one(related="checklist_id.repair_id", store=True, readonly=True)
    sequence = fields.Integer(default=10)
    phase = fields.Selection(PHASE_SELECTION, required=True, default="identification")
    name = fields.Char(string="Contrôle", required=True)
    expected_criteria = fields.Text(string="Critère attendu")
    instruction = fields.Text(string="Instruction atelier")
    measurement_type = fields.Selection(MEASUREMENT_TYPE_SELECTION, default="boolean", required=True)
    is_measurement_entered = fields.Boolean(string="Mesure saisie")
    measured_value = fields.Float(string="Valeur mesurée")
    measured_text = fields.Char(string="Texte mesuré / référence")
    unit = fields.Char(string="Unité")
    use_min_value = fields.Boolean(string="Seuil minimum actif")
    min_value = fields.Float(string="Seuil minimum")
    use_max_value = fields.Boolean(string="Seuil maximum actif")
    max_value = fields.Float(string="Seuil maximum")
    verdict = fields.Selection(VERDICT_SELECTION, default="pending", string="Verdict", required=True)
    comment = fields.Text(string="Commentaire")
    required = fields.Boolean(string="Obligatoire", default=True)
    blocking = fields.Boolean(string="Bloquant", default=False)
    requires_photo_on_fail = fields.Boolean(string="Photo obligatoire si non conforme", default=True)
    proof_attachment_ids = fields.Many2many("ir.attachment", string="Preuves / photos")
    proof_attachment_count = fields.Integer(string="Preuves", compute="_compute_proof_attachment_count")
    diagnostic_ids = fields.One2many("sav.battery.diagnostic", "checklist_line_id", string="Diagnostics")
    diagnostic_count = fields.Integer(string="Diagnostics", compute="_compute_diagnostic_count")
    is_out_of_range = fields.Boolean(string="Hors seuil", compute="_compute_is_out_of_range", store=True)
    is_complete = fields.Boolean(string="Contrôle complété", compute="_compute_is_complete", store=True)

    def _compute_proof_attachment_count(self):
        for line in self:
            line.proof_attachment_count = len(line.proof_attachment_ids)

    @api.depends("diagnostic_ids")
    def _compute_diagnostic_count(self):
        for line in self:
            line.diagnostic_count = len(line.diagnostic_ids)

    @api.depends("measurement_type", "is_measurement_entered", "measured_value", "use_min_value", "min_value", "use_max_value", "max_value")
    def _compute_is_out_of_range(self):
        for line in self:
            if line.measurement_type == "numeric" and line.is_measurement_entered:
                line.is_out_of_range = (line.use_min_value and line.measured_value < line.min_value) or (line.use_max_value and line.measured_value > line.max_value)
            else:
                line.is_out_of_range = False

    @api.depends("verdict", "measurement_type", "is_measurement_entered", "measured_text", "proof_attachment_ids")
    def _compute_is_complete(self):
        for line in self:
            if line.verdict == "pending":
                line.is_complete = False
            elif line.verdict == "na":
                line.is_complete = True
            elif line.measurement_type == "numeric":
                line.is_complete = bool(line.is_measurement_entered)
            elif line.measurement_type == "text":
                line.is_complete = bool(line.measured_text or line.comment)
            elif line.measurement_type == "photo":
                line.is_complete = bool(line.proof_attachment_ids)
            else:
                line.is_complete = True

    def _auto_numeric_verdict_values(self, vals):
        current = self if len(self) == 1 else False
        measurement_type = vals.get("measurement_type") or (current.measurement_type if current else False)
        if measurement_type != "numeric":
            return vals
        is_entered = vals.get("is_measurement_entered") if "is_measurement_entered" in vals else (current.is_measurement_entered if current else False)
        if not is_entered:
            return vals
        if vals.get("verdict") == "na":
            return vals
        measured_value = vals.get("measured_value") if "measured_value" in vals else (current.measured_value if current else 0.0)
        use_min = vals.get("use_min_value") if "use_min_value" in vals else (current.use_min_value if current else False)
        min_value = vals.get("min_value") if "min_value" in vals else (current.min_value if current else 0.0)
        use_max = vals.get("use_max_value") if "use_max_value" in vals else (current.use_max_value if current else False)
        max_value = vals.get("max_value") if "max_value" in vals else (current.max_value if current else 0.0)
        if (use_min and measured_value < min_value) or (use_max and measured_value > max_value):
            vals["verdict"] = "fail"
        else:
            vals["verdict"] = "pass"
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        prepared = []
        dummy = self.browse()
        for vals in vals_list:
            prepared.append(dummy._auto_numeric_verdict_values(dict(vals)))
        return super().create(prepared)

    def write(self, vals):
        if {"measured_value", "is_measurement_entered", "min_value", "max_value", "use_min_value", "use_max_value", "measurement_type"} & set(vals):
            for line in self:
                line_vals = line._auto_numeric_verdict_values(dict(vals))
                super(SavBatteryChecklistLine, line).write(line_vals)
            return True
        return super().write(vals)

    @api.onchange("measured_value")
    def _onchange_measured_value_mark_entered(self):
        for line in self:
            if line.measurement_type == "numeric":
                line.is_measurement_entered = True

    @api.onchange("measured_value", "min_value", "max_value", "use_min_value", "use_max_value", "measurement_type", "is_measurement_entered")
    def _onchange_measured_value(self):
        for line in self:
            if line.measurement_type == "numeric" and line.is_measurement_entered:
                if (line.use_min_value and line.measured_value < line.min_value) or (line.use_max_value and line.measured_value > line.max_value):
                    line.verdict = "fail"
                else:
                    line.verdict = "pass"

    @api.constrains("verdict", "comment", "requires_photo_on_fail", "proof_attachment_ids")
    def _check_fail_requirements(self):
        for line in self:
            if line.verdict == "fail" and not line.comment:
                raise ValidationError(_("Un contrôle non conforme doit avoir un commentaire."))
            if line.verdict == "fail" and line.requires_photo_on_fail and not line.proof_attachment_ids:
                raise ValidationError(_("Un contrôle critique non conforme doit avoir une preuve photo ou pièce jointe."))

    def action_pass(self):
        self.write({"verdict": "pass", "is_measurement_entered": True})
        return True

    def action_fail(self):
        self.write({"verdict": "fail"})
        return True

    def action_na(self):
        self.write({"verdict": "na"})
        return True

    def action_pending(self):
        self.write({"verdict": "pending"})
        return True

    def action_create_diagnostic(self):
        self.ensure_one()
        if self.verdict != "fail":
            raise ValidationError(_("Un diagnostic ne peut être créé que pour un contrôle non conforme."))
        diagnostic = self.env["sav.battery.diagnostic"].get_or_create_from_checklist_line(self)
        return {
            "type": "ir.actions.act_window",
            "name": _("Diagnostic batterie"),
            "res_model": "sav.battery.diagnostic",
            "res_id": diagnostic.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_open_diagnostics(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Diagnostics batterie"),
            "res_model": "sav.battery.diagnostic",
            "view_mode": "list,form",
            "domain": [("checklist_line_id", "=", self.id)],
            "context": {"default_repair_id": self.repair_id.id, "default_checklist_id": self.checklist_id.id, "default_checklist_line_id": self.id},
        }
