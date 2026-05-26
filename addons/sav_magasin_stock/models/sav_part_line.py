from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavMagasinSavPartLine(models.Model):
    _inherit = "sav.magasin.part.line"

    state = fields.Selection(
        selection_add=[
            ("transfer_requested", "Transfert demandé"),
            ("purchase_needed", "Commande à prévoir"),
        ],
        ondelete={
            "transfer_requested": "set default",
            "purchase_needed": "set default",
        },
    )
    local_available_qty = fields.Float(string="Stock local", compute="_compute_stock_info")
    total_available_qty = fields.Float(string="Stock total", compute="_compute_stock_info")
    remote_available_qty = fields.Float(string="Stock distant", compute="_compute_stock_info")
    source_warehouse_id = fields.Many2one("stock.warehouse", string="Source distante", compute="_compute_stock_info")
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
    reserved_for_sav = fields.Boolean(string="Réservé pour dossier batterie")
    reserved_date = fields.Datetime(string="Date réservation", readonly=True)
    consumed_date = fields.Datetime(string="Date consommation", readonly=True)
    stock_decision_note = fields.Char(string="Note décision stock", compute="_compute_stock_decision_note", store=False)
    stock_action_required = fields.Selection(
        [
            ("reserve", "Réserver localement"),
            ("transfer", "Demander transfert"),
            ("purchase", "Commander fournisseur"),
            ("none", "Aucune action"),
        ],
        string="Action recommandée",
        compute="_compute_stock_decision_note",
        store=False,
    )

    @api.depends("product_id", "quantity", "order_id.warehouse_id")
    def _compute_stock_info(self):
        Warehouse = self.env["stock.warehouse"]
        for line in self:
            product = line.product_id
            line.source_warehouse_id = False
            if not product:
                line.local_available_qty = 0
                line.total_available_qty = 0
                line.remote_available_qty = 0
                line.availability_state = "unknown"
                continue

            total_qty = product.qty_available
            warehouse = line.order_id.warehouse_id
            if warehouse and warehouse.lot_stock_id:
                local_qty = product.with_context(location=warehouse.lot_stock_id.id).qty_available
            else:
                local_qty = total_qty

            remote_qty = max(total_qty - local_qty, 0)
            line.local_available_qty = local_qty
            line.total_available_qty = total_qty
            line.remote_available_qty = remote_qty

            if local_qty >= line.quantity:
                line.availability_state = "available_local"
            elif total_qty >= line.quantity:
                line.availability_state = "available_remote"
                remote_warehouses = Warehouse.search([
                    ("id", "!=", warehouse.id if warehouse else 0),
                    ("company_id", "=", line.order_id.company_id.id if line.order_id.company_id else self.env.company.id),
                ])
                for remote_warehouse in remote_warehouses:
                    qty = product.with_context(location=remote_warehouse.lot_stock_id.id).qty_available if remote_warehouse.lot_stock_id else 0
                    if qty >= line.quantity:
                        line.source_warehouse_id = remote_warehouse
                        break
            else:
                line.availability_state = "missing"

    @api.depends("availability_state", "local_available_qty", "remote_available_qty", "quantity", "reserved_for_sav", "source_warehouse_id")
    def _compute_stock_decision_note(self):
        for line in self:
            if line.reserved_for_sav:
                line.stock_decision_note = _("Composant batterie réservée métier pour ce dossier.")
                line.stock_action_required = "none"
            elif line.availability_state == "available_local":
                line.stock_decision_note = _("Stock local suffisant : réserver ou sortir la composant batterie.")
                line.stock_action_required = "reserve"
            elif line.availability_state == "available_remote":
                if line.source_warehouse_id:
                    line.stock_decision_note = _("Stock distant disponible dans %s : prévoir un transfert.") % line.source_warehouse_id.display_name
                else:
                    line.stock_decision_note = _("Stock distant disponible : prévoir transfert inter-stock.")
                line.stock_action_required = "transfer"
            elif line.availability_state == "missing":
                line.stock_decision_note = _("Stock insuffisant : commande fournisseur à prévoir.")
                line.stock_action_required = "purchase"
            else:
                line.stock_decision_note = _("Sélectionner un article pour vérifier le stock.")
                line.stock_action_required = "none"

    def action_check_stock(self):
        for line in self:
            message = line.stock_decision_note or _("Stock vérifié.")
            if line.order_id:
                line.order_id.message_post(body=_("Vérification stock pour %s : %s") % (line.product_id.display_name, message))
        return True

    def action_mark_reserved(self):
        for line in self:
            if not line.product_id:
                raise ValidationError(_("Sélectionner un article avant de réserver."))
            if line.availability_state == "missing":
                raise ValidationError(_("Stock insuffisant : réserver impossible. Utiliser un transfert, une commande ou un substitut."))
            values = {"reserved_for_sav": True, "reserved_date": fields.Datetime.now(), "state": "reserved"}
            line.write(values)
            if line.order_id:
                line.order_id.message_post(body=_("Composant batterie réservée pour dossier batterie : %s x %s.") % (line.quantity, line.product_id.display_name))
        return True

    def action_request_transfer(self):
        for line in self:
            if line.availability_state != "available_remote":
                raise ValidationError(_("Le transfert n'est pertinent que si le stock distant est disponible."))
            line.write({"state": "transfer_requested"})
            if line.order_id:
                source = line.source_warehouse_id.display_name if line.source_warehouse_id else _("stock distant")
                line.order_id.message_post(body=_("Transfert demandé pour %s depuis %s.") % (line.product_id.display_name, source))
                if line.order_id.state in ("diagnosis", "repair"):
                    line.order_id.action_wait_part()
        return True

    def action_request_purchase(self):
        for line in self:
            line.write({"state": "purchase_needed"})
            if line.order_id:
                line.order_id.message_post(body=_("Commande fournisseur à prévoir pour %s.") % line.product_id.display_name)
                if line.order_id.state in ("diagnosis", "repair"):
                    line.order_id.action_wait_part()
        return True

    def action_mark_consumed(self):
        for line in self:
            line.write({"state": "consumed", "consumed_date": fields.Datetime.now()})
            if line.order_id:
                line.order_id.message_post(body=_("Composant batterie consommée sur le dossier : %s x %s.") % (line.quantity, line.product_id.display_name))
        return True

    def action_unreserve(self):
        for line in self:
            line.write({"reserved_for_sav": False, "reserved_date": False, "state": "to_check"})
            if line.order_id:
                line.order_id.message_post(body=_("Réservation métier annulée pour %s.") % line.product_id.display_name)
        return True
