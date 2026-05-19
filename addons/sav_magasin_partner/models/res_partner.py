from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sav_magasin_customer_type = fields.Selection(
        [
            ("b2c", "Particulier"),
            ("b2b", "Professionnel"),
            ("unknown", "À qualifier"),
        ],
        string="Type client SAV",
        default="unknown",
    )
    sav_magasin_billing_partner_id = fields.Many2one("res.partner", string="Client facturé par défaut")
    sav_magasin_delivery_partner_id = fields.Many2one("res.partner", string="Client livré par défaut")
    sav_magasin_internal_note = fields.Text(string="Note accueil magasin")
    sav_magasin_duplicate_score = fields.Integer(string="Score doublon", compute="_compute_sav_magasin_duplicate_score")
    sav_magasin_has_minimum_contact = fields.Boolean(string="Contact minimum présent", compute="_compute_sav_magasin_has_minimum_contact")

    def _sav_magasin_mobile_value(self):
        """Return mobile value only when the current Odoo version exposes the field.

        Some Odoo Community images do not expose res.partner.mobile.
        The module must therefore not declare it in @api.depends and must not
        search on it unless the field exists in the registry.
        """
        self.ensure_one()
        if "mobile" in self._fields:
            return self.mobile
        return False

    @api.depends("phone", "email")
    def _compute_sav_magasin_has_minimum_contact(self):
        for partner in self:
            partner.sav_magasin_has_minimum_contact = bool(
                partner.phone or partner.email or partner._sav_magasin_mobile_value()
            )

    @api.depends("phone", "email")
    def _compute_sav_magasin_duplicate_score(self):
        mobile_field_available = "mobile" in self._fields
        for partner in self:
            score = 0
            domain = [("id", "!=", partner.id)]
            if partner.email:
                score += self.search_count(domain + [("email", "=", partner.email)], limit=1) * 50
            if partner.phone:
                score += self.search_count(domain + [("phone", "=", partner.phone)], limit=1) * 25
            if mobile_field_available and partner._sav_magasin_mobile_value():
                score += self.search_count(domain + [("mobile", "=", partner._sav_magasin_mobile_value())], limit=1) * 25
            partner.sav_magasin_duplicate_score = min(score, 100)
