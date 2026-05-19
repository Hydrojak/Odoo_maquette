from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SavMagasinSavCreateWizard(models.TransientModel):
    _name = "sav.magasin.create.wizard"
    _description = "Assistant de création rapide dossier SAV"

    partner_id = fields.Many2one("res.partner", string="Client existant")
    create_partner = fields.Boolean(string="Créer un nouveau client")
    new_partner_name = fields.Char(string="Nom du client")
    new_partner_phone = fields.Char(string="Téléphone")
    new_partner_email = fields.Char(string="Email")
    customer_type = fields.Selection(
        [("b2c", "Particulier"), ("b2b", "Professionnel"), ("unknown", "À qualifier")],
        string="Type client",
        default="b2c",
    )

    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Magasin",
        default=lambda self: self.env["stock.warehouse"].search([("company_id", "=", self.env.company.id)], limit=1),
    )
    technician_id = fields.Many2one("res.users", string="Technicien")
    priority = fields.Selection([("0", "Normal"), ("1", "Urgent"), ("2", "Critique")], default="0")

    device_name = fields.Char(string="Produit déposé")
    brand_id = fields.Many2one("sav.magasin.product.brand", string="Marque")
    range_id = fields.Many2one("sav.magasin.product.range", string="Gamme")
    model_id = fields.Many2one("sav.magasin.device.model", string="Modèle")
    serial_number = fields.Char(string="Numéro de série")
    warranty_state = fields.Selection(
        [("unknown", "À vérifier"), ("in_warranty", "Sous garantie"), ("out_warranty", "Hors garantie")],
        string="Garantie",
        default="unknown",
    )

    symptom = fields.Text(string="Symptôme client")
    visual_state = fields.Selection(
        [
            ("good", "Bon état apparent"),
            ("scratched", "Rayé"),
            ("broken", "Cassé / endommagé"),
            ("incomplete", "Incomplet"),
            ("unknown", "À vérifier"),
            ("other", "Autre"),
        ],
        string="État visuel",
        default="unknown",
    )
    visual_state_note = fields.Text(string="Précision état visuel")
    acc_charger = fields.Boolean(string="Chargeur")
    acc_cable = fields.Boolean(string="Câble")
    acc_battery = fields.Boolean(string="Batterie")
    acc_bag = fields.Boolean(string="Sacoche / housse")
    acc_other = fields.Char(string="Autre accessoire")

    def _prepare_accessories_text(self):
        self.ensure_one()
        labels = []
        if self.acc_charger:
            labels.append(_("Chargeur"))
        if self.acc_cable:
            labels.append(_("Câble"))
        if self.acc_battery:
            labels.append(_("Batterie"))
        if self.acc_bag:
            labels.append(_("Sacoche / housse"))
        if self.acc_other:
            labels.append(self.acc_other)
        return ", ".join(labels) if labels else _("Aucun accessoire déclaré")

    def _prepare_visual_state_text(self):
        self.ensure_one()
        label = dict(self._fields["visual_state"].selection).get(self.visual_state, "")
        if self.visual_state_note:
            return "%s - %s" % (label, self.visual_state_note)
        return label

    def _get_or_create_partner(self):
        self.ensure_one()
        if self.partner_id and not self.create_partner:
            return self.partner_id
        if not self.new_partner_name:
            raise ValidationError(_("Renseignez un client existant ou le nom du nouveau client."))
        if not (self.new_partner_phone or self.new_partner_email):
            raise ValidationError(_("Le téléphone ou l'email du client est obligatoire."))
        values = {
            "name": self.new_partner_name,
            "phone": self.new_partner_phone,
            "email": self.new_partner_email,
            "customer_rank": 1,
        }
        if "sav_magasin_customer_type" in self.env["res.partner"]._fields:
            values["sav_magasin_customer_type"] = self.customer_type
        return self.env["res.partner"].create(values)

    def action_create_sav_order(self):
        self.ensure_one()
        if not self.device_name:
            raise ValidationError(_("Le produit déposé est obligatoire."))
        if not self.symptom:
            raise ValidationError(_("Le symptôme client est obligatoire."))
        if not self.warehouse_id:
            raise ValidationError(_("Le magasin est obligatoire."))
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
            "serial_number": self.serial_number,
            "warranty_state": self.warranty_state,
            "symptom": self.symptom,
            "visual_state": self._prepare_visual_state_text(),
            "accessories": self._prepare_accessories_text(),
        })
        order.action_validate_deposit()
        return {
            "type": "ir.actions.act_window",
            "name": _("Dossier SAV"),
            "res_model": "sav.magasin.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }
