from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SavMagasinSavOrder(models.Model):
    _name = "sav.magasin.order"
    _description = "Dossier SAV magasin"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(default="Nouveau", readonly=True, copy=False, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("new", "Nouveau"),
            ("diagnosis", "Diagnostic"),
            ("customer_wait", "Attente client"),
            ("part_wait", "Attente pièce"),
            ("repair", "Réparation"),
            ("ready", "Prêt à restituer"),
            ("invoiced", "Facturé"),
            ("returned", "Restitué"),
            ("closed", "Clôturé"),
            ("cancelled", "Annulé"),
        ],
        default="draft",
        tracking=True,
        required=True,
    )
    partner_id = fields.Many2one("res.partner", string="Client", tracking=True, required=True)
    billing_partner_id = fields.Many2one("res.partner", string="Client facturé")
    delivered_partner_id = fields.Many2one("res.partner", string="Client livré")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Magasin",
        tracking=True,
        default=lambda self: self._default_warehouse_id(),
    )
    user_id = fields.Many2one("res.users", string="Responsable", default=lambda self: self.env.user, tracking=True)
    technician_id = fields.Many2one("res.users", string="Technicien", tracking=True)
    deposit_date = fields.Datetime(string="Date dépôt", default=fields.Datetime.now, tracking=True)
    promised_date = fields.Datetime(string="Date prévue")
    return_date = fields.Datetime(string="Date restitution", tracking=True)
    priority = fields.Selection([("0", "Normal"), ("1", "Urgent"), ("2", "Critique")], default="0")

    device_name = fields.Char(string="Produit déposé", required=True, tracking=True)
    brand_id = fields.Many2one("sav.magasin.product.brand", string="Marque")
    range_id = fields.Many2one("sav.magasin.product.range", string="Gamme")
    model_id = fields.Many2one("sav.magasin.device.model", string="Modèle")
    serial_number = fields.Char(string="Numéro de série")
    warranty_state = fields.Selection(
        [("unknown", "À vérifier"), ("in_warranty", "Sous garantie"), ("out_warranty", "Hors garantie")],
        string="Garantie",
        default="unknown",
        tracking=True,
    )

    symptom = fields.Text(string="Symptôme client", required=True)
    visual_state = fields.Text(string="État visuel")
    accessories = fields.Text(string="Accessoires déposés")
    diagnosis = fields.Text(string="Diagnostic")
    repair_note = fields.Text(string="Compte-rendu réparation")
    customer_note = fields.Text(string="Information client")

    part_line_ids = fields.One2many("sav.magasin.part.line", "order_id", string="Pièces")
    amount_parts = fields.Monetary(string="Montant pièces", compute="_compute_amounts", store=True)
    amount_labor = fields.Monetary(string="Main-d'œuvre")
    amount_total = fields.Monetary(string="Total estimé", compute="_compute_amounts", store=True)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", readonly=True)
    invoice_id = fields.Many2one("account.move", string="Facture")
    sale_order_id = fields.Many2one("sale.order", string="Devis / commande")

    kanban_color = fields.Integer(string="Couleur kanban", compute="_compute_kanban_color")
    is_open = fields.Boolean(string="Dossier ouvert", compute="_compute_is_open", search="_search_is_open")
    contact_warning = fields.Char(string="Alerte contact", compute="_compute_contact_warning")

    @api.model
    def _default_warehouse_id(self):
        warehouse = self.env["stock.warehouse"].search([("company_id", "=", self.env.company.id)], limit=1)
        return warehouse.id or False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = self.env["ir.sequence"].next_by_code("sav.magasin.order") or "Nouveau"
        orders = super().create(vals_list)
        for order in orders:
            order.message_post(body=_("Dossier SAV créé."))
        return orders

    @api.depends("part_line_ids.subtotal", "amount_labor")
    def _compute_amounts(self):
        for order in self:
            order.amount_parts = sum(order.part_line_ids.mapped("subtotal"))
            order.amount_total = order.amount_parts + order.amount_labor

    @api.depends("state")
    def _compute_kanban_color(self):
        color_by_state = {
            "draft": 0,
            "new": 2,
            "diagnosis": 3,
            "customer_wait": 4,
            "part_wait": 1,
            "repair": 6,
            "ready": 10,
            "invoiced": 7,
            "returned": 9,
            "closed": 9,
            "cancelled": 8,
        }
        for order in self:
            order.kanban_color = color_by_state.get(order.state, 0)

    @api.depends("state")
    def _compute_is_open(self):
        for order in self:
            order.is_open = order.state not in ("closed", "cancelled")

    def _search_is_open(self, operator, value):
        open_states = ["draft", "new", "diagnosis", "customer_wait", "part_wait", "repair", "ready", "invoiced", "returned"]
        if (operator in ("=", "==") and value) or (operator in ("!=", "<>") and not value):
            return [("state", "in", open_states)]
        return [("state", "not in", open_states)]

    @api.depends("partner_id", "partner_id.phone", "partner_id.email")
    def _compute_contact_warning(self):
        for order in self:
            if order.partner_id and not self._partner_has_minimum_contact(order.partner_id):
                order.contact_warning = _("Le client n'a ni téléphone ni email renseigné.")
            else:
                order.contact_warning = False

    def _partner_has_minimum_contact(self, partner):
        mobile = partner["mobile"] if "mobile" in partner._fields else False
        return bool(partner.phone or partner.email or mobile)

    def _ensure_required_for_deposit(self):
        for order in self:
            missing = []
            if not order.partner_id:
                missing.append(_("Client"))
            elif not order._partner_has_minimum_contact(order.partner_id):
                missing.append(_("Téléphone ou email client"))
            if not order.device_name:
                missing.append(_("Produit déposé"))
            if not order.symptom:
                missing.append(_("Symptôme client"))
            if not order.visual_state:
                missing.append(_("État visuel"))
            if not order.warehouse_id:
                missing.append(_("Magasin"))
            if missing:
                raise ValidationError(_("Impossible de valider le dépôt. Champs manquants : %s") % ", ".join(missing))

    def _set_state(self, state, message):
        for order in self:
            order.state = state
            order.message_post(body=message)
        return True

    def action_validate_deposit(self):
        self._ensure_required_for_deposit()
        return self._set_state("new", _("Dépôt validé."))

    def action_start_diagnosis(self):
        return self._set_state("diagnosis", _("Diagnostic lancé."))

    def action_wait_customer(self):
        return self._set_state("customer_wait", _("Dossier mis en attente client."))

    def action_wait_part(self):
        return self._set_state("part_wait", _("Dossier mis en attente pièce."))

    def action_start_repair(self):
        return self._set_state("repair", _("Réparation démarrée."))

    def action_ready(self):
        return self._set_state("ready", _("Dossier prêt à restituer."))

    def action_mark_invoiced(self):
        return self._set_state("invoiced", _("Dossier marqué comme facturé."))

    def action_returned(self):
        self.write({"state": "returned", "return_date": fields.Datetime.now()})
        self.message_post(body=_("Produit restitué au client."))
        return True

    def action_close(self):
        return self._set_state("closed", _("Dossier clôturé."))

    def action_cancel(self):
        return self._set_state("cancelled", _("Dossier annulé."))

    def action_reset_to_draft(self):
        return self._set_state("draft", _("Dossier remis en brouillon."))

    def action_print_deposit(self):
        return self.env.ref("sav_magasin_core.action_report_sav_magasin_sav_deposit").report_action(self)

    def action_open_customer(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Client"),
            "res_model": "res.partner",
            "res_id": self.partner_id.id,
            "view_mode": "form",
            "target": "current",
        }


class SavMagasinSavPartLine(models.Model):
    _name = "sav.magasin.part.line"
    _description = "Ligne pièce SAV"
    _order = "order_id, sequence, id"

    sequence = fields.Integer(default=10)
    order_id = fields.Many2one("sav.magasin.order", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Article / pièce", required=True)
    name = fields.Char(string="Description")
    quantity = fields.Float(default=1.0, required=True)
    price_unit = fields.Monetary(string="Prix unitaire")
    subtotal = fields.Monetary(compute="_compute_subtotal", store=True)
    currency_id = fields.Many2one(related="order_id.currency_id", readonly=True)
    note = fields.Char()

    @api.onchange("product_id")
    def _onchange_product_id(self):
        for line in self:
            if line.product_id:
                line.name = line.product_id.display_name
                line.price_unit = line.product_id.lst_price

    @api.constrains("quantity")
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_("La quantité de pièce doit être supérieure à zéro."))

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
