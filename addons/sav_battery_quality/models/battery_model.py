from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavBatteryModel(models.Model):
    _name = "sav.battery.model"
    _description = "Modèle batterie atelier"
    _order = "name"

    name = fields.Char(string="Modèle batterie", required=True)
    active = fields.Boolean(default=True)

    nominal_voltage = fields.Float(string="Tension nominale (V)", required=True)
    max_voltage = fields.Float(string="Tension maximale (V)", required=True)
    capacity_ah = fields.Float(string="Capacité (Ah)")
    chemistry = fields.Selection(
        [
            ("li_ion", "Li-ion"),
            ("lifepo4", "LiFePO4"),
            ("nimh", "NiMH"),
            ("lead", "Plomb"),
            ("other", "Autre"),
        ],
        string="Chimie",
        default="li_ion",
        required=True,
    )
    series_count = fields.Integer(string="Cellules en série")
    parallel_count = fields.Integer(string="Cellules en parallèle")
    architecture = fields.Char(string="Architecture S/P", compute="_compute_architecture", store=True)
    bms_type = fields.Char(string="Type de BMS")
    connector_type = fields.Char(string="Connectique")
    charger_voltage = fields.Float(string="Tension chargeur (V)")
    note = fields.Text(string="Note technique")

    is_under_60v = fields.Boolean(string="Compatible < 60 V", compute="_compute_is_under_60v", store=True)

    @api.depends("series_count", "parallel_count")
    def _compute_architecture(self):
        for record in self:
            if record.series_count and record.parallel_count:
                record.architecture = "%sS%sP" % (record.series_count, record.parallel_count)
            elif record.series_count:
                record.architecture = "%sS" % record.series_count
            else:
                record.architecture = False

    @api.depends("max_voltage")
    def _compute_is_under_60v(self):
        for record in self:
            record.is_under_60v = bool(record.max_voltage and record.max_voltage < 60.0)

    @api.constrains("nominal_voltage", "max_voltage", "charger_voltage")
    def _check_voltage_limit(self):
        for record in self:
            if record.nominal_voltage and record.nominal_voltage >= 60.0:
                raise ValidationError(_("La tension nominale d’un modèle batterie Re-Watt doit être strictement inférieure à 60 V."))
            if record.max_voltage and record.max_voltage >= 60.0:
                raise ValidationError(_("La tension maximale d’un modèle batterie Re-Watt doit être strictement inférieure à 60 V."))
            if record.charger_voltage and record.charger_voltage >= 60.0:
                raise ValidationError(_("La tension chargeur renseignée doit être strictement inférieure à 60 V pour ce workflow."))
            if record.max_voltage and record.nominal_voltage and record.max_voltage < record.nominal_voltage:
                raise ValidationError(_("La tension maximale ne peut pas être inférieure à la tension nominale."))
