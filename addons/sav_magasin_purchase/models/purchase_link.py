from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sav_order_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", index=True, copy=False)
    sav_part_line_count = fields.Integer(string="Lignes batterie", compute="_compute_sav_part_line_count")

    @api.depends("order_line.sav_part_line_id")
    def _compute_sav_part_line_count(self):
        for order in self:
            order.sav_part_line_count = len(order.order_line.filtered(lambda line: line.sav_part_line_id))

    def action_open_sav_order(self):
        self.ensure_one()
        if not self.sav_order_id:
            return False
        return {
            "type": "ir.actions.act_window",
            "name": _("Dossier batterie"),
            "res_model": "sav.magasin.order",
            "res_id": self.sav_order_id.id,
            "view_mode": "form",
            "target": "current",
        }


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    sav_order_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", index=True, copy=False)
    sav_part_line_id = fields.Many2one("sav.magasin.part.line", string="Ligne composant batterie", index=True, copy=False)


class SavMagasinOrder(models.Model):
    _inherit = "sav.magasin.order"

    purchase_order_count = fields.Integer(string="Commandes fournisseur", compute="_compute_purchase_order_info")
    purchase_to_receive_count = fields.Integer(string="Commandes à recevoir", compute="_compute_purchase_order_info")
    purchase_attention = fields.Char(string="Suivi achats", compute="_compute_purchase_order_info")

    def _get_purchase_orders(self):
        self.ensure_one()
        PurchaseOrder = self.env["purchase.order"]
        orders = PurchaseOrder.search(["|", ("sav_order_id", "=", self.id), ("order_line.sav_order_id", "=", self.id)])
        return orders

    def _compute_purchase_order_info(self):
        for order in self:
            purchase_orders = order._get_purchase_orders()
            order.purchase_order_count = len(purchase_orders)
            pending = purchase_orders.filtered(lambda po: po.state not in ("cancel", "done"))
            order.purchase_to_receive_count = len(pending)
            waiting_lines = order.part_line_ids.filtered(lambda line: line.state in ("purchase_needed", "purchase_ordered"))
            if waiting_lines:
                order.purchase_attention = _("%s ligne(s) composant batterie en suivi achat.") % len(waiting_lines)
            elif pending:
                order.purchase_attention = _("%s commande(s) fournisseur en cours.") % len(pending)
            else:
                order.purchase_attention = False

    def action_open_purchase_orders(self):
        self.ensure_one()
        orders = self._get_purchase_orders()
        return {
            "type": "ir.actions.act_window",
            "name": _("Commandes fournisseur batterie"),
            "res_model": "purchase.order",
            "view_mode": "list,form",
            "domain": [("id", "in", orders.ids)],
            "context": {"default_sav_order_id": self.id},
            "target": "current",
        }


class SavMagasinPartLine(models.Model):
    _inherit = "sav.magasin.part.line"

    state = fields.Selection(
        selection_add=[
            ("purchase_ordered", "Commande créée"),
            ("received", "Reçue"),
        ],
        ondelete={
            "purchase_ordered": "set default",
            "received": "set default",
        },
    )
    vendor_id = fields.Many2one("res.partner", string="Fournisseur", domain=[("supplier_rank", ">", 0)])
    purchase_order_id = fields.Many2one("purchase.order", string="Commande fournisseur", readonly=True, copy=False)
    purchase_order_line_id = fields.Many2one("purchase.order.line", string="Ligne commande", readonly=True, copy=False)
    purchase_created_date = fields.Datetime(string="Date commande", readonly=True, copy=False)
    expected_receipt_date = fields.Datetime(string="Réception prévue")
    purchase_state = fields.Selection(related="purchase_order_id.state", string="Statut achat", readonly=True)
    purchase_note = fields.Char(string="Note achat")

    def _get_default_vendor(self):
        self.ensure_one()
        if self.vendor_id:
            return self.vendor_id
        product = self.product_id
        sellers = product.seller_ids if product and "seller_ids" in product._fields else self.env["product.supplierinfo"]
        seller = sellers[:1]
        return seller.partner_id if seller else False

    def _prepare_purchase_order_vals(self, vendor):
        self.ensure_one()
        vals = {
            "partner_id": vendor.id,
            "sav_order_id": self.order_id.id,
            "origin": self.order_id.name,
        }
        if "company_id" in self.env["purchase.order"]._fields and self.order_id.company_id:
            vals["company_id"] = self.order_id.company_id.id
        if "date_planned" in self.env["purchase.order"]._fields and self.expected_receipt_date:
            vals["date_planned"] = self.expected_receipt_date
        return vals

    def _prepare_purchase_order_line_vals(self, order):
        self.ensure_one()
        product = self.product_id
        POL = self.env["purchase.order.line"]
        vals = {
            "order_id": order.id,
            "product_id": product.id,
            "name": self.name or product.display_name,
            "product_qty": self.quantity,
            "price_unit": product.standard_price or self.price_unit or 0.0,
            "sav_order_id": self.order_id.id,
            "sav_part_line_id": self.id,
        }
        if "product_uom" in POL._fields:
            uom = product.uom_po_id if "uom_po_id" in product._fields and product.uom_po_id else product.uom_id
            vals["product_uom"] = uom.id
        if "date_planned" in POL._fields:
            vals["date_planned"] = self.expected_receipt_date or fields.Datetime.now()
        if "company_id" in POL._fields and self.order_id.company_id:
            vals["company_id"] = self.order_id.company_id.id
        return vals

    def action_create_purchase_order(self):
        PurchaseOrder = self.env["purchase.order"]
        PurchaseOrderLine = self.env["purchase.order.line"]
        created_orders = self.env["purchase.order"]
        for line in self:
            if not line.product_id:
                raise ValidationError(_("Sélectionner une composant batterie avant de créer une commande fournisseur."))
            if line.purchase_order_id:
                created_orders |= line.purchase_order_id
                continue
            vendor = line._get_default_vendor()
            if not vendor:
                raise ValidationError(_("Aucun fournisseur défini pour %s. Renseignez un fournisseur sur la ligne composant batterie ou sur l'article.") % line.product_id.display_name)
            order = PurchaseOrder.create(line._prepare_purchase_order_vals(vendor))
            order_line = PurchaseOrderLine.create(line._prepare_purchase_order_line_vals(order))
            line.write({
                "vendor_id": vendor.id,
                "purchase_order_id": order.id,
                "purchase_order_line_id": order_line.id,
                "purchase_created_date": fields.Datetime.now(),
                "state": "purchase_ordered",
            })
            if line.order_id:
                if line.order_id.state in ("diagnosis", "repair"):
                    line.order_id.action_wait_part()
                line.order_id.message_post(body=_("Commande fournisseur créée pour %s : %s.") % (line.product_id.display_name, order.name))
            created_orders |= order
        if len(created_orders) == 1:
            return {
                "type": "ir.actions.act_window",
                "name": _("Commande fournisseur"),
                "res_model": "purchase.order",
                "res_id": created_orders.id,
                "view_mode": "form",
                "target": "current",
            }
        return {
            "type": "ir.actions.act_window",
            "name": _("Commandes fournisseur créées"),
            "res_model": "purchase.order",
            "view_mode": "list,form",
            "domain": [("id", "in", created_orders.ids)],
            "target": "current",
        }

    def action_open_purchase_order(self):
        self.ensure_one()
        if not self.purchase_order_id:
            raise ValidationError(_("Aucune commande fournisseur n'est liée à cette ligne."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Commande fournisseur"),
            "res_model": "purchase.order",
            "res_id": self.purchase_order_id.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_mark_received(self):
        for line in self:
            line.write({"state": "received"})
            if line.order_id:
                line.order_id.message_post(body=_("Composant batterie reçue pour le dossier : %s x %s.") % (line.quantity, line.product_id.display_name))
        return True
