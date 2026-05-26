from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavMagasinProductSubstitution(models.Model):
    _name = "sav.magasin.product.substitution"
    _description = "Substitution composant batterie"
    _order = "sequence, id"

    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Libellé", compute="_compute_name", store=True)
    original_product_id = fields.Many2one("product.product", string="Article d'origine", required=True, ondelete="cascade")
    substitute_product_id = fields.Many2one("product.product", string="Article substitut", required=True, ondelete="restrict")
    substitution_type = fields.Selection(
        [
            ("equivalent", "Équivalent"),
            ("compatible", "Compatible"),
            ("upgrade", "Supérieur"),
            ("downgrade", "Dégradé"),
            ("temporary", "Dépannage temporaire"),
        ],
        string="Type",
        default="compatible",
        required=True,
    )
    validation_state = fields.Selection(
        [
            ("validated", "Validé"),
            ("to_test", "À tester"),
            ("restricted", "Validation responsable"),
            ("forbidden", "Interdit"),
        ],
        string="Statut validation",
        default="validated",
        required=True,
    )
    priority = fields.Integer(string="Priorité", default=10)
    price_policy = fields.Selection(
        [
            ("same", "Même prix"),
            ("substitute", "Prix du substitut"),
            ("manual", "Prix manuel"),
        ],
        string="Politique prix",
        default="substitute",
    )
    warranty_impact = fields.Selection(
        [
            ("same", "Garantie identique"),
            ("reduced", "Garantie réduite"),
            ("extended", "Garantie étendue"),
            ("none", "Aucune garantie"),
            ("confirm", "À confirmer"),
        ],
        string="Impact garantie",
        default="same",
    )
    technical_note = fields.Text(string="Note technique")
    substitute_available_qty = fields.Float(string="Stock substitut", compute="_compute_substitute_stock")

    @api.depends("original_product_id", "substitute_product_id", "substitution_type")
    def _compute_name(self):
        for record in self:
            if record.original_product_id and record.substitute_product_id:
                record.name = _("%s → %s") % (record.original_product_id.display_name, record.substitute_product_id.display_name)
            else:
                record.name = False

    @api.depends("substitute_product_id")
    def _compute_substitute_stock(self):
        for record in self:
            record.substitute_available_qty = record.substitute_product_id.qty_available if record.substitute_product_id else 0.0

    @api.constrains("original_product_id", "substitute_product_id")
    def _check_distinct_products(self):
        for record in self:
            if record.original_product_id and record.original_product_id == record.substitute_product_id:
                raise ValidationError(_("Un article ne peut pas être son propre substitut."))

    def action_disable(self):
        self.write({"active": False})
        return True


class ProductProduct(models.Model):
    _inherit = "product.product"

    sav_substitution_line_ids = fields.One2many(
        "sav.magasin.product.substitution",
        "original_product_id",
        string="Substituts batterie",
    )
    sav_substitution_count = fields.Integer(string="Substituts", compute="_compute_sav_substitution_count")

    def _compute_sav_substitution_count(self):
        for product in self:
            product.sav_substitution_count = len(product.sav_substitution_line_ids)

    def action_open_sav_substitutions(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Substituts batterie"),
            "res_model": "sav.magasin.product.substitution",
            "view_mode": "list,form",
            "domain": [("original_product_id", "=", self.id)],
            "context": {"default_original_product_id": self.id},
        }
