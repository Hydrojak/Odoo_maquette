from odoo import _, fields, models
from odoo.exceptions import ValidationError


class SavMagasinOrderRepair(models.Model):
    _inherit = "sav.magasin.order"

    device_product_id = fields.Many2one(
        "product.product",
        string="Produit Odoo à réparer",
        help="Produit Odoo utilisé pour créer l'ordre de réparation standard. L'ancien ERP identifiait souvent le produit en texte libre ; ce champ permet de raccrocher le dossier au moteur Repair d'Odoo.",
    )
    repair_order_id = fields.Many2one("repair.order", string="Ordre de réparation batterie", copy=False, readonly=True)
    repair_order_count = fields.Integer(string="Réparations", compute="_compute_repair_order_count")
    repair_state = fields.Char(string="Statut réparation batterie Odoo", compute="_compute_repair_state")

    def _compute_repair_order_count(self):
        for order in self:
            order.repair_order_count = 1 if order.repair_order_id else 0

    def _compute_repair_state(self):
        for order in self:
            repair = order.repair_order_id
            if not repair:
                order.repair_state = False
                continue
            if "state" in repair._fields:
                raw_state = repair.state
                selection = dict(repair._fields["state"].selection)
                order.repair_state = selection.get(raw_state, raw_state)
            else:
                order.repair_state = repair.display_name

    def _get_repair_product(self):
        self.ensure_one()
        product = self.device_product_id
        if not product and self.part_line_ids:
            product = self.part_line_ids[:1].product_id
        return product

    def _prepare_repair_order_values(self):
        self.ensure_one()
        RepairOrder = self.env["repair.order"]
        repair_fields = RepairOrder._fields
        vals = {}

        product = self._get_repair_product()
        if "product_id" in repair_fields:
            if not product and repair_fields["product_id"].required:
                raise ValidationError(_("Sélectionner un Produit Odoo à réparer avant de créer l'ordre de réparation."))
            if product:
                vals["product_id"] = product.id

        mapping = {
            "partner_id": self.partner_id.id,
            "company_id": self.company_id.id,
            "user_id": (self.technician_id or self.user_id).id,
            "sale_order_id": self.sale_order_id.id,
        }
        for field_name, value in mapping.items():
            if field_name in repair_fields and value:
                vals[field_name] = value

        if product:
            if "product_qty" in repair_fields:
                vals["product_qty"] = 1.0
            if "product_uom" in repair_fields and product.uom_id:
                vals["product_uom"] = product.uom_id.id
            if "product_uom_id" in repair_fields and product.uom_id:
                vals["product_uom_id"] = product.uom_id.id

        if "picking_type_id" in repair_fields:
            picking_type = self.env["stock.picking.type"].search([
                ("code", "=", "repair_operation"),
                ("company_id", "in", [self.company_id.id, False]),
            ], limit=1)
            if picking_type:
                vals["picking_type_id"] = picking_type.id

        if "origin" in repair_fields:
            vals["origin"] = self.name
        if "name" in repair_fields:
            vals.setdefault("name", _("Réparation %s") % self.name)
        if "schedule_date" in repair_fields:
            vals["schedule_date"] = fields.Datetime.now()
        if "description" in repair_fields:
            vals["description"] = self._build_repair_description()
        if "internal_notes" in repair_fields:
            vals["internal_notes"] = self._build_repair_description()
        if "location_id" in repair_fields and self.warehouse_id and self.warehouse_id.lot_stock_id:
            vals["location_id"] = self.warehouse_id.lot_stock_id.id

        return vals

    def _build_repair_description(self):
        self.ensure_one()
        lines = [
            _("Dossier batterie : %s") % self.name,
            _("Batterie : %s") % (self.device_name or ""),
            _("Symptôme client : %s") % (self.symptom or ""),
        ]
        if self.diagnosis:
            lines.append(_("Diagnostic : %s") % self.diagnosis)
        if self.visual_state:
            lines.append(_("État visuel : %s") % self.visual_state)
        if self.accessories:
            lines.append(_("Accessoires : %s") % self.accessories)
        return "\n".join(lines)

    def action_create_repair_order(self):
        for order in self:
            if order.repair_order_id:
                continue
            vals = order._prepare_repair_order_values()
            repair = self.env["repair.order"].create(vals)
            order.write({"repair_order_id": repair.id})
            order.message_post(body=_("Ordre de réparation batterie Odoo créé : %s.") % repair.display_name)
            if order.state in ("new", "diagnosis", "part_wait"):
                order.action_start_repair()
        return self.action_open_repair_order()

    def action_open_repair_order(self):
        self.ensure_one()
        if not self.repair_order_id:
            return self.action_create_repair_order()
        return {
            "type": "ir.actions.act_window",
            "name": _("Ordre de réparation batterie"),
            "res_model": "repair.order",
            "view_mode": "form",
            "res_id": self.repair_order_id.id,
            "target": "current",
        }
