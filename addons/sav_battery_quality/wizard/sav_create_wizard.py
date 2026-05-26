from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavMagasinCreateWizardBattery(models.TransientModel):
    _inherit = "sav.magasin.create.wizard"

    battery_model_id = fields.Many2one("sav.battery.model", string="Modèle batterie")
    battery_serial = fields.Char(string="Numéro série batterie")
    battery_nominal_voltage = fields.Float(string="Tension nominale (V)")
    battery_max_voltage = fields.Float(string="Tension maximale (V)")
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
    bms_type = fields.Char(string="Type de BMS")
    connector_type = fields.Char(string="Connectique")
    charger_voltage = fields.Float(string="Tension chargeur (V)")

    @api.onchange("battery_model_id")
    def _onchange_battery_model_id(self):
        for wizard in self:
            model = wizard.battery_model_id
            if not model:
                continue
            wizard.battery_nominal_voltage = model.nominal_voltage
            wizard.battery_max_voltage = model.max_voltage
            wizard.battery_capacity_ah = model.capacity_ah
            wizard.battery_chemistry = model.chemistry
            wizard.battery_series_count = model.series_count
            wizard.battery_parallel_count = model.parallel_count
            wizard.bms_type = model.bms_type
            wizard.connector_type = model.connector_type
            wizard.charger_voltage = model.charger_voltage
            if not wizard.device_name:
                wizard.device_name = model.name

    def _create_order(self):
        self.ensure_one()
        if not self.device_name:
            raise ValidationError(_("La batterie est obligatoire."))
        if not self.symptom:
            raise ValidationError(_("Le symptôme client est obligatoire."))
        if not self.warehouse_id:
            raise ValidationError(_("Le magasin est obligatoire."))
        if not self.battery_nominal_voltage:
            raise ValidationError(_("La tension nominale batterie est obligatoire."))
        if not self.battery_max_voltage:
            raise ValidationError(_("La tension maximale batterie est obligatoire."))
        if self.battery_max_voltage >= 60.0:
            raise ValidationError(_("Batterie hors périmètre : tension maximale >= 60 V."))
        if self.charger_voltage and self.charger_voltage >= 60.0:
            raise ValidationError(_("Chargeur hors périmètre : tension >= 60 V."))

        partner = self._get_or_create_partner()
        order = self.env["sav.magasin.order"].create({
            "partner_id": partner.id,
            "billing_partner_id": partner.id,
            "delivered_partner_id": partner.id,
            "warehouse_id": self.warehouse_id.id,
            "technician_id": self.technician_id.id,
            "priority": self.priority,
            "device_name": self.device_name,
            "brand_id": self.brand_id.id,
            "range_id": self.range_id.id,
            "model_id": self.model_id.id,
            "serial_number": self.serial_number or self.battery_serial,
            "warranty_state": self.warranty_state,
            "symptom": self.symptom,
            "visual_state": self._prepare_visual_state_text(),
            "accessories": self._prepare_accessories_text(),
            "internal_note": self.internal_note,
            "is_battery_repair": True,
            "battery_model_id": self.battery_model_id.id,
            "battery_serial": self.battery_serial or self.serial_number,
            "battery_nominal_voltage": self.battery_nominal_voltage,
            "battery_max_voltage": self.battery_max_voltage,
            "battery_capacity_ah": self.battery_capacity_ah,
            "battery_chemistry": self.battery_chemistry,
            "battery_series_count": self.battery_series_count,
            "battery_parallel_count": self.battery_parallel_count,
            "bms_type": self.bms_type,
            "connector_type": self.connector_type,
            "charger_voltage": self.charger_voltage,
        })
        order.action_validate_deposit()
        return order
