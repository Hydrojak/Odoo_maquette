from odoo import fields, models


class SavMagasinProductBrand(models.Model):
    _name = "sav.magasin.product.brand"
    _description = "Marque produit"
    _order = "name"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    note = fields.Text()


class SavMagasinProductRange(models.Model):
    _name = "sav.magasin.product.range"
    _description = "Gamme produit"
    _order = "name"

    name = fields.Char(required=True)
    brand_id = fields.Many2one("sav.magasin.product.brand", string="Marque")
    active = fields.Boolean(default=True)
    note = fields.Text()


class SavMagasinDeviceModel(models.Model):
    _name = "sav.magasin.device.model"
    _description = "Modèle appareil"
    _order = "brand_id, range_id, name"

    name = fields.Char(required=True)
    brand_id = fields.Many2one("sav.magasin.product.brand", string="Marque")
    range_id = fields.Many2one("sav.magasin.product.range", string="Gamme")
    active = fields.Boolean(default=True)
    note = fields.Text()


class SavMagasinArticleType(models.Model):
    _name = "sav.magasin.article.type"
    _description = "Type article métier"
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    code = fields.Char()
    requires_serial = fields.Boolean(string="Numéro de série requis")
    stock_managed = fields.Boolean(string="Géré en stock", default=True)
    active = fields.Boolean(default=True)
