from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavMagasinSavPartLine(models.Model):
    _inherit = "sav.magasin.part.line"

    state = fields.Selection(
        selection_add=[("substituted", "Substituée")],
        ondelete={"substituted": "set default"},
    )
    substitution_count = fields.Integer(string="Substituts", compute="_compute_substitution_info")
    suggested_substitution_id = fields.Many2one(
        "sav.magasin.product.substitution",
        string="Substitut suggéré",
        compute="_compute_substitution_info",
    )
    suggested_substitute_product_id = fields.Many2one(
        "product.product",
        string="Produit substitut suggéré",
        compute="_compute_substitution_info",
    )
    suggested_substitute_available_qty = fields.Float(
        string="Stock substitut suggéré",
        compute="_compute_substitution_info",
    )
    substitution_decision_note = fields.Char(string="Note substitution", compute="_compute_substitution_info")

    @api.depends("product_id", "quantity")
    def _compute_substitution_info(self):
        Substitution = self.env["sav.magasin.product.substitution"]
        for line in self:
            line.substitution_count = 0
            line.suggested_substitution_id = False
            line.suggested_substitute_product_id = False
            line.suggested_substitute_available_qty = 0.0
            line.substitution_decision_note = False
            if not line.product_id:
                continue

            substitutions = Substitution.search([
                ("active", "=", True),
                ("original_product_id", "=", line.product_id.id),
                ("validation_state", "!=", "forbidden"),
            ], order="priority, sequence, id")
            line.substitution_count = len(substitutions)
            suggested = False
            for substitution in substitutions:
                qty = substitution.substitute_product_id.qty_available
                if qty >= line.quantity:
                    suggested = substitution
                    break
            if not suggested and substitutions:
                suggested = substitutions[0]
            if suggested:
                qty = suggested.substitute_product_id.qty_available
                line.suggested_substitution_id = suggested
                line.suggested_substitute_product_id = suggested.substitute_product_id
                line.suggested_substitute_available_qty = qty
                if qty >= line.quantity and suggested.validation_state == "validated":
                    line.substitution_decision_note = _("Substitut validé disponible : %s") % suggested.substitute_product_id.display_name
                elif qty >= line.quantity:
                    line.substitution_decision_note = _("Substitut disponible mais validation à contrôler : %s") % suggested.substitute_product_id.display_name
                else:
                    line.substitution_decision_note = _("Substitut connu mais stock insuffisant : %s") % suggested.substitute_product_id.display_name

    def action_use_suggested_substitute(self):
        for line in self:
            if not line.suggested_substitution_id or not line.suggested_substitute_product_id:
                raise ValidationError(_("Aucun substitut disponible pour cette ligne."))
            original = line.product_id.display_name
            substitute = line.suggested_substitute_product_id.display_name
            if line.suggested_substitution_id.validation_state == "forbidden":
                raise ValidationError(_("Le substitut sélectionné est interdit."))
            line.write({
                "product_id": line.suggested_substitute_product_id.id,
                "name": line.suggested_substitute_product_id.display_name,
                "price_unit": line.suggested_substitute_product_id.lst_price,
                "state": "substituted",
                "note": _("Substitution appliquée : %s remplacé par %s") % (original, substitute),
            })
            if line.order_id:
                line.order_id.message_post(body=_("Substitution appliquée : %s remplacé par %s.") % (original, substitute))
        return True
