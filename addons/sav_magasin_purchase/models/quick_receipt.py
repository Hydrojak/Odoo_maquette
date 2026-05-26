from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavMagasinQuickReceipt(models.Model):
    _name = "sav.magasin.quick.receipt"
    _description = "Réception sans commande"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(default="Nouvelle réception", readonly=True, copy=False)
    state = fields.Selection([("draft", "Brouillon"), ("checked", "Contrôlé"), ("done", "Validé"), ("cancelled", "Annulé")], default="draft", tracking=True)
    partner_id = fields.Many2one("res.partner", string="Fournisseur", required=True)
    warehouse_id = fields.Many2one("stock.warehouse", string="Magasin", required=True)
    receipt_date = fields.Datetime(default=fields.Datetime.now, required=True)
    delivery_note = fields.Char(string="Bon de livraison")
    vendor_bill_ref = fields.Char(string="Facture fournisseur")
    sav_order_id = fields.Many2one("sav.magasin.order", string="Dossier batterie lié")
    line_ids = fields.One2many("sav.magasin.quick.receipt.line", "receipt_id", string="Lignes")
    note = fields.Text()
    received_part_line_count = fields.Integer(string="Lignes batterie reçues", compute="_compute_received_part_line_count")


    @api.model
    def _ensure_sequence_and_next(self):
        sequence = self.env["ir.sequence"].sudo().search([("code", "=", "sav.magasin.quick.receipt")], limit=1)
        if not sequence:
            sequence = self.env["ir.sequence"].sudo().create({
                "name": "Réception sans commande batterie",
                "code": "sav.magasin.quick.receipt",
                "prefix": "REC%(y)s",
                "padding": 5,
                "company_id": False,
            })
        return sequence.next_by_id() or "Nouvelle réception"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouvelle réception") == "Nouvelle réception":
                vals["name"] = self.env["ir.sequence"].next_by_code("sav.magasin.quick.receipt") or self._ensure_sequence_and_next()
        return super().create(vals_list)

    @api.depends("line_ids.sav_part_line_id")
    def _compute_received_part_line_count(self):
        for receipt in self:
            receipt.received_part_line_count = len(receipt.line_ids.filtered(lambda line: line.sav_part_line_id))

    def action_check(self):
        for receipt in self:
            if not receipt.line_ids:
                raise ValidationError(_("Ajoutez au moins une ligne de réception."))
            for line in receipt.line_ids:
                if line.quantity <= 0:
                    raise ValidationError(_("La quantité doit être positive."))
                if not line.product_id:
                    raise ValidationError(_("Chaque ligne doit avoir un article."))
            receipt.state = "checked"

    def action_validate(self):
        for receipt in self:
            if receipt.state == "draft":
                receipt.action_check()
            receipt.message_post(body=_("Réception validée. Les lignes batterie rattachées sont marquées comme reçues."))
            receipt.state = "done"
            linked_orders = self.env["sav.magasin.order"]
            for line in receipt.line_ids.filtered("sav_part_line_id"):
                line.sav_part_line_id.action_mark_received()
                linked_orders |= line.sav_part_line_id.order_id
            for order in linked_orders:
                order.message_post(body=_("Réception fournisseur %s validée pour une ou plusieurs composants batterie du dossier.") % receipt.name)
        return True

    def action_cancel(self):
        self.write({"state": "cancelled"})


class SavMagasinQuickReceiptLine(models.Model):
    _name = "sav.magasin.quick.receipt.line"
    _description = "Ligne réception sans commande"
    _order = "receipt_id, sequence, id"

    sequence = fields.Integer(default=10)
    receipt_id = fields.Many2one("sav.magasin.quick.receipt", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Article", required=True)
    quantity = fields.Float(default=1.0, required=True)
    price_unit = fields.Monetary(string="Prix achat")
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    location_hint = fields.Char(string="Localisation")
    sav_order_id = fields.Many2one(related="receipt_id.sav_order_id", store=True, readonly=True)
    sav_part_line_id = fields.Many2one("sav.magasin.part.line", string="Ligne composant batterie")
    purchase_order_id = fields.Many2one("purchase.order", related="sav_part_line_id.purchase_order_id", string="Commande fournisseur", readonly=True)
    note = fields.Char()

    @api.onchange("sav_part_line_id")
    def _onchange_sav_part_line_id(self):
        for line in self:
            if line.sav_part_line_id:
                part_line = line.sav_part_line_id
                line.product_id = part_line.product_id
                line.quantity = part_line.quantity
                line.price_unit = part_line.product_id.standard_price or part_line.price_unit
