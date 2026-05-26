from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    sav_order_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", index=True, copy=False)
    sav_part_line_id = fields.Many2one("sav.magasin.part.line", string="Ligne composant batterie", index=True, copy=False)
    sav_quick_receipt_id = fields.Many2one("sav.magasin.quick.receipt", string="Réception batterie", index=True, copy=False)

    def action_open_sav_order(self):
        self.ensure_one()
        order = self.sav_order_id or self.sav_part_line_id.order_id or self.sav_quick_receipt_id.sav_order_id
        if not order:
            return False
        return {
            "type": "ir.actions.act_window",
            "name": _("Dossier batterie"),
            "res_model": "sav.magasin.order",
            "res_id": order.id,
            "view_mode": "form",
            "target": "current",
        }


class StockMove(models.Model):
    _inherit = "stock.move"

    sav_order_id = fields.Many2one("sav.magasin.order", string="Dossier batterie", index=True, copy=False)
    sav_part_line_id = fields.Many2one("sav.magasin.part.line", string="Ligne composant batterie", index=True, copy=False)
    sav_quick_receipt_id = fields.Many2one("sav.magasin.quick.receipt", string="Réception batterie", index=True, copy=False)


class SavMagasinPartLine(models.Model):
    _inherit = "sav.magasin.part.line"

    stock_reservation_picking_id = fields.Many2one("stock.picking", string="Réservation stock", readonly=True, copy=False)
    stock_transfer_picking_id = fields.Many2one("stock.picking", string="Transfert stock", readonly=True, copy=False)
    stock_consumption_picking_id = fields.Many2one("stock.picking", string="Sortie composant batterie", readonly=True, copy=False)
    stock_picking_count = fields.Integer(string="Flux stock", compute="_compute_stock_flow_info")
    stock_flow_state_note = fields.Char(string="Suivi flux stock", compute="_compute_stock_flow_info")

    @api.depends("stock_reservation_picking_id.state", "stock_transfer_picking_id.state", "stock_consumption_picking_id.state")
    def _compute_stock_flow_info(self):
        for line in self:
            pickings = line._get_stock_pickings()
            line.stock_picking_count = len(pickings)
            if not pickings:
                line.stock_flow_state_note = False
                continue
            states = ", ".join(sorted(set(pickings.mapped("state"))))
            line.stock_flow_state_note = _("%s flux stock lié(s) : %s") % (len(pickings), states)

    def _get_stock_pickings(self):
        self.ensure_one()
        pickings = self.env["stock.picking"]
        for field_name in ("stock_reservation_picking_id", "stock_transfer_picking_id", "stock_consumption_picking_id"):
            picking = self[field_name]
            if picking:
                pickings |= picking
        extra = self.env["stock.picking"].search([("sav_part_line_id", "=", self.id)])
        return pickings | extra

    def _get_customer_location(self):
        self.ensure_one()
        partner = self.order_id.partner_id
        if partner and "property_stock_customer" in partner._fields and partner.property_stock_customer:
            return partner.property_stock_customer
        location = self.env.ref("stock.stock_location_customers", raise_if_not_found=False)
        if not location:
            raise ValidationError(_("Emplacement client introuvable. Vérifiez le module Stock."))
        return location

    def _get_supplier_location(self):
        self.ensure_one()
        partner = self.vendor_id if "vendor_id" in self._fields and self.vendor_id else False
        if partner and "property_stock_supplier" in partner._fields and partner.property_stock_supplier:
            return partner.property_stock_supplier
        location = self.env.ref("stock.stock_location_suppliers", raise_if_not_found=False)
        if not location:
            raise ValidationError(_("Emplacement fournisseur introuvable. Vérifiez le module Stock."))
        return location

    def _require_warehouse_locations(self):
        self.ensure_one()
        warehouse = self.order_id.warehouse_id
        if not warehouse or not warehouse.lot_stock_id:
            raise ValidationError(_("Le dossier batterie doit être rattaché à un magasin avec un emplacement de stock."))
        return warehouse

    def _picking_vals(self, picking_type, source_location, dest_location, origin_suffix=None):
        self.ensure_one()
        if not picking_type:
            raise ValidationError(_("Type d'opération stock introuvable pour ce magasin."))
        vals = {
            "picking_type_id": picking_type.id,
            "location_id": source_location.id,
            "location_dest_id": dest_location.id,
            "origin": "%s%s" % (self.order_id.name, " - " + origin_suffix if origin_suffix else ""),
            "sav_order_id": self.order_id.id,
            "sav_part_line_id": self.id,
        }
        if "partner_id" in self.env["stock.picking"]._fields and self.order_id.partner_id:
            vals["partner_id"] = self.order_id.partner_id.id
        if "company_id" in self.env["stock.picking"]._fields and self.order_id.company_id:
            vals["company_id"] = self.order_id.company_id.id
        return vals

    def _move_vals(self, picking, source_location, dest_location, description=None):
        self.ensure_one()
        Move = self.env["stock.move"]
        product = self.product_id
        if not product:
            raise ValidationError(_("Sélectionner une composant batterie avant de créer un flux stock."))
        vals = {
            "name": description or self.name or product.display_name,
            "picking_id": picking.id,
            "product_id": product.id,
            "location_id": source_location.id,
            "location_dest_id": dest_location.id,
            "sav_order_id": self.order_id.id,
            "sav_part_line_id": self.id,
        }
        if "product_uom_qty" in Move._fields:
            vals["product_uom_qty"] = self.quantity
        elif "product_qty" in Move._fields:
            vals["product_qty"] = self.quantity
        elif "quantity" in Move._fields:
            vals["quantity"] = self.quantity
        if "product_uom" in Move._fields:
            vals["product_uom"] = product.uom_id.id
        if "company_id" in Move._fields and self.order_id.company_id:
            vals["company_id"] = self.order_id.company_id.id
        if "origin" in Move._fields:
            vals["origin"] = self.order_id.name
        return vals

    def _confirm_and_assign_picking(self, picking):
        if picking.state == "draft" and hasattr(picking, "action_confirm"):
            picking.action_confirm()
        if hasattr(picking, "action_assign"):
            try:
                picking.action_assign()
            except Exception:
                # La création du flux doit rester exploitable même si la réservation automatique échoue.
                pass
        return picking

    def _create_stock_picking_with_move(self, picking_type, source_location, dest_location, description, origin_suffix=None):
        self.ensure_one()
        Picking = self.env["stock.picking"]
        Move = self.env["stock.move"]
        picking = Picking.create(self._picking_vals(picking_type, source_location, dest_location, origin_suffix=origin_suffix))
        Move.create(self._move_vals(picking, source_location, dest_location, description=description))
        self._confirm_and_assign_picking(picking)
        return picking

    def action_open_stock_pickings(self):
        self.ensure_one()
        pickings = self._get_stock_pickings()
        return {
            "type": "ir.actions.act_window",
            "name": _("Flux stock batterie"),
            "res_model": "stock.picking",
            "view_mode": "list,form",
            "domain": [("id", "in", pickings.ids)],
            "target": "current",
        }

    def action_mark_reserved(self):
        result_action = False
        for line in self:
            if line.stock_reservation_picking_id:
                result_action = line.action_open_stock_pickings()
                continue
            if line.availability_state == "missing":
                raise ValidationError(_("Stock insuffisant : réserver impossible. Utiliser un transfert, une commande ou un substitut."))
            warehouse = line._require_warehouse_locations()
            source = warehouse.lot_stock_id
            destination = line._get_customer_location()
            picking_type = warehouse.out_type_id
            picking = line._create_stock_picking_with_move(
                picking_type,
                source,
                destination,
                _("Réservation composant batterie - %s") % line.product_id.display_name,
                origin_suffix=_("Réservation composant batterie"),
            )
            line.write({
                "reserved_for_sav": True,
                "reserved_date": fields.Datetime.now(),
                "state": "reserved",
                "stock_reservation_picking_id": picking.id,
            })
            if line.order_id:
                line.order_id.message_post(body=_("Flux de réservation stock créé pour %s : %s.") % (line.product_id.display_name, picking.name))
            result_action = line.action_open_stock_pickings()
        return result_action or True

    def action_request_transfer(self):
        result_action = False
        for line in self:
            if line.stock_transfer_picking_id:
                result_action = line.action_open_stock_pickings()
                continue
            if line.availability_state != "available_remote" and not line.source_warehouse_id:
                raise ValidationError(_("Le transfert nécessite un stock distant disponible."))
            dest_warehouse = line._require_warehouse_locations()
            source_warehouse = line.source_warehouse_id
            if not source_warehouse or not source_warehouse.lot_stock_id:
                raise ValidationError(_("Aucun magasin source distant n'est identifié pour cette composant batterie."))
            picking_type = source_warehouse.int_type_id or dest_warehouse.int_type_id
            picking = line._create_stock_picking_with_move(
                picking_type,
                source_warehouse.lot_stock_id,
                dest_warehouse.lot_stock_id,
                _("Transfert composant batterie - %s") % line.product_id.display_name,
                origin_suffix=_("Transfert composant batterie"),
            )
            line.write({"state": "transfer_requested", "stock_transfer_picking_id": picking.id})
            if line.order_id:
                line.order_id.message_post(body=_("Transfert stock créé pour %s : %s.") % (line.product_id.display_name, picking.name))
                if line.order_id.state in ("diagnosis", "repair"):
                    line.order_id.action_wait_part()
            result_action = line.action_open_stock_pickings()
        return result_action or True

    def action_mark_consumed(self):
        result_action = False
        for line in self:
            picking = line.stock_consumption_picking_id or line.stock_reservation_picking_id
            if picking and picking.state == "done":
                line.write({"state": "consumed", "consumed_date": fields.Datetime.now()})
                if line.order_id:
                    line.order_id.message_post(body=_("Composant batterie consommée sur le dossier : %s x %s.") % (line.quantity, line.product_id.display_name))
                continue
            if not picking:
                warehouse = line._require_warehouse_locations()
                picking = line._create_stock_picking_with_move(
                    warehouse.out_type_id,
                    warehouse.lot_stock_id,
                    line._get_customer_location(),
                    _("Sortie composant batterie - %s") % line.product_id.display_name,
                    origin_suffix=_("Sortie composant batterie"),
                )
                line.write({"stock_consumption_picking_id": picking.id, "state": "reserved"})
                if line.order_id:
                    line.order_id.message_post(body=_("Sortie stock préparée pour %s : %s. Valider le transfert dans Stock pour consommer réellement la composant batterie.") % (line.product_id.display_name, picking.name))
            result_action = line.action_open_stock_pickings()
        return result_action or True

    def action_refresh_stock_flow_status(self):
        for line in self:
            if line.stock_consumption_picking_id and line.stock_consumption_picking_id.state == "done":
                line.write({"state": "consumed", "consumed_date": fields.Datetime.now()})
            elif line.stock_reservation_picking_id and line.stock_reservation_picking_id.state == "done":
                line.write({"state": "consumed", "consumed_date": fields.Datetime.now()})
            elif line.stock_transfer_picking_id and line.stock_transfer_picking_id.state == "done":
                line.write({"state": "reserved", "reserved_for_sav": True, "reserved_date": fields.Datetime.now()})
            if line.order_id:
                line.order_id.message_post(body=_("Statut stock synchronisé pour %s.") % (line.product_id.display_name or line.name))
        return True


class SavMagasinQuickReceipt(models.Model):
    _inherit = "sav.magasin.quick.receipt"

    stock_picking_id = fields.Many2one("stock.picking", string="Réception stock", readonly=True, copy=False)

    def _create_incoming_picking(self):
        self.ensure_one()
        if self.stock_picking_id:
            return self.stock_picking_id
        if not self.warehouse_id or not self.warehouse_id.lot_stock_id:
            raise ValidationError(_("La réception doit être rattachée à un magasin avec emplacement de stock."))
        if not self.line_ids:
            raise ValidationError(_("Ajoutez au moins une ligne de réception."))
        picking_type = self.warehouse_id.in_type_id
        if not picking_type:
            raise ValidationError(_("Type de réception introuvable pour ce magasin."))
        supplier_location = self.partner_id.property_stock_supplier if "property_stock_supplier" in self.partner_id._fields and self.partner_id.property_stock_supplier else self.env.ref("stock.stock_location_suppliers", raise_if_not_found=False)
        if not supplier_location:
            raise ValidationError(_("Emplacement fournisseur introuvable."))
        Picking = self.env["stock.picking"]
        Move = self.env["stock.move"]
        picking_vals = {
            "picking_type_id": picking_type.id,
            "location_id": supplier_location.id,
            "location_dest_id": self.warehouse_id.lot_stock_id.id,
            "origin": self.name,
            "partner_id": self.partner_id.id,
            "sav_order_id": self.sav_order_id.id if self.sav_order_id else False,
            "sav_quick_receipt_id": self.id,
        }
        if "company_id" in Picking._fields:
            picking_vals["company_id"] = self.env.company.id
        picking = Picking.create(picking_vals)
        for line in self.line_ids:
            vals = {
                "name": line.product_id.display_name,
                "picking_id": picking.id,
                "product_id": line.product_id.id,
                "location_id": supplier_location.id,
                "location_dest_id": self.warehouse_id.lot_stock_id.id,
                "sav_order_id": line.sav_part_line_id.order_id.id if line.sav_part_line_id else (self.sav_order_id.id if self.sav_order_id else False),
                "sav_part_line_id": line.sav_part_line_id.id if line.sav_part_line_id else False,
                "sav_quick_receipt_id": self.id,
            }
            if "product_uom_qty" in Move._fields:
                vals["product_uom_qty"] = line.quantity
            elif "product_qty" in Move._fields:
                vals["product_qty"] = line.quantity
            elif "quantity" in Move._fields:
                vals["quantity"] = line.quantity
            if "product_uom" in Move._fields:
                vals["product_uom"] = line.product_id.uom_id.id
            if "company_id" in Move._fields:
                vals["company_id"] = self.env.company.id
            move = Move.create(vals)
            line.write({"stock_move_id": move.id})
        if picking.state == "draft" and hasattr(picking, "action_confirm"):
            picking.action_confirm()
        self.stock_picking_id = picking.id
        return picking

    def action_validate(self):
        for receipt in self:
            if receipt.state == "draft":
                receipt.action_check()
            picking = receipt._create_incoming_picking()
            receipt.message_post(body=_("Réception stock créée : %s. Valider l'opération dans Stock pour mettre à jour physiquement les quantités.") % picking.name)
        return super().action_validate()

    def action_open_stock_picking(self):
        self.ensure_one()
        if not self.stock_picking_id:
            raise ValidationError(_("Aucune réception stock liée."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Réception stock"),
            "res_model": "stock.picking",
            "res_id": self.stock_picking_id.id,
            "view_mode": "form",
            "target": "current",
        }


class SavMagasinQuickReceiptLine(models.Model):
    _inherit = "sav.magasin.quick.receipt.line"

    stock_move_id = fields.Many2one("stock.move", string="Mouvement stock", readonly=True, copy=False)
