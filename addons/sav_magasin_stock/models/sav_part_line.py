from odoo import api, fields, models


class SavMagasinSavPartLine(models.Model):
    _inherit = "sav.magasin.part.line"

    local_available_qty = fields.Float(string="Stock local", compute="_compute_stock_info")
    total_available_qty = fields.Float(string="Stock total", compute="_compute_stock_info")
    availability_state = fields.Selection(
        [
            ("available_local", "Disponible localement"),
            ("available_remote", "Disponible à distance"),
            ("missing", "À commander"),
            ("unknown", "À vérifier"),
        ],
        string="Décision stock",
        compute="_compute_stock_info",
    )
    reserved_for_sav = fields.Boolean(string="Réservé pour SAV")
    stock_decision_note = fields.Char(string="Note décision stock")

    @api.depends("product_id", "quantity", "order_id.warehouse_id")
    def _compute_stock_info(self):
        for line in self:
            product = line.product_id
            if not product:
                line.local_available_qty = 0
                line.total_available_qty = 0
                line.availability_state = "unknown"
                continue
            line.total_available_qty = product.qty_available
            local_qty = 0
            warehouse = line.order_id.warehouse_id
            if warehouse and warehouse.lot_stock_id:
                local_qty = product.with_context(location=warehouse.lot_stock_id.id).qty_available
            else:
                local_qty = product.qty_available
            line.local_available_qty = local_qty
            if local_qty >= line.quantity:
                line.availability_state = "available_local"
            elif product.qty_available >= line.quantity:
                line.availability_state = "available_remote"
            else:
                line.availability_state = "missing"

    def action_mark_reserved(self):
        self.write({"reserved_for_sav": True, "stock_decision_note": "Réservation métier à matérialiser par mouvement stock."})
