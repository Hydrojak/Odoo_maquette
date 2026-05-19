from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sav_magasin_brand_id = fields.Many2one("sav.magasin.product.brand", string="Marque")
    sav_magasin_range_id = fields.Many2one("sav.magasin.product.range", string="Gamme")
    sav_magasin_model_id = fields.Many2one("sav.magasin.device.model", string="Modèle")
    sav_magasin_article_type_id = fields.Many2one("sav.magasin.article.type", string="Type article")
    sav_magasin_supplier_reference = fields.Char(string="Référence fournisseur")
    sav_magasin_manufacturer_reference = fields.Char(string="Référence constructeur")
    sav_magasin_location_hint = fields.Char(string="Localisation magasin")
    sav_magasin_equivalent_product_ids = fields.Many2many(
        "product.template",
        "sav_magasin_product_equivalence_rel",
        "src_product_id",
        "equivalent_product_id",
        string="Articles équivalents",
    )
    sav_magasin_completeness_state = fields.Selection(
        [
            ("incomplete", "Incomplet"),
            ("to_check", "À contrôler"),
            ("complete", "Complet"),
        ],
        compute="_compute_sav_magasin_completeness_state",
        store=True,
        default="incomplete",
    )
    sav_magasin_notes = fields.Text(string="Notes métier")

    @api.depends("name", "list_price", "standard_price", "sav_magasin_article_type_id", "sav_magasin_brand_id")
    def _compute_sav_magasin_completeness_state(self):
        for product in self:
            missing = []
            if not product.name:
                missing.append("name")
            if not product.sav_magasin_article_type_id:
                missing.append("article_type")
            product_type = False
            if "type" in product._fields:
                product_type = product.type
            elif "detailed_type" in product._fields:
                product_type = product.detailed_type

            if product_type in ("product", "storable") and not product.sav_magasin_brand_id:
                missing.append("brand")
            if missing:
                product.sav_magasin_completeness_state = "incomplete"
            elif product.list_price <= 0:
                product.sav_magasin_completeness_state = "to_check"
            else:
                product.sav_magasin_completeness_state = "complete"
