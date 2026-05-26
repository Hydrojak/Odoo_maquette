from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SavMagasinSavOrder(models.Model):
    _name = "sav.magasin.order"
    _description = "Dossier atelier batterie"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"

    name = fields.Char(default="Nouveau", readonly=True, copy=False, tracking=True)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("new", "Dépôt validé"),
            ("diagnosis", "Diagnostic"),
            ("customer_wait", "Attente client"),
            ("part_wait", "Attente composant batterie"),
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
    deposit_validated_date = fields.Datetime(string="Date validation dépôt", readonly=True)
    diagnosis_date = fields.Datetime(string="Date diagnostic", readonly=True)
    repair_start_date = fields.Datetime(string="Date début réparation", readonly=True)
    ready_date = fields.Datetime(string="Date prêt à restituer", readonly=True)
    return_date = fields.Datetime(string="Date restitution", tracking=True)
    closed_date = fields.Datetime(string="Date clôture", readonly=True)
    promised_date = fields.Datetime(string="Date prévue")
    priority = fields.Selection([("0", "Normal"), ("1", "Urgent"), ("2", "Critique")], default="0", tracking=True)

    device_name = fields.Char(string="Batterie", required=True, tracking=True)
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
    internal_note = fields.Text(string="Note interne")

    part_line_ids = fields.One2many("sav.magasin.part.line", "order_id", string="Composants batterie")
    part_line_count = fields.Integer(string="Nombre de lignes composants batterie", compute="_compute_part_line_count")
    amount_parts = fields.Monetary(string="Montant composants batterie", compute="_compute_amounts", store=True)
    amount_labor = fields.Monetary(string="Main-d'œuvre")
    amount_total = fields.Monetary(string="Total estimé", compute="_compute_amounts", store=True)
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", readonly=True)
    invoice_id = fields.Many2one("account.move", string="Facture")
    sale_order_id = fields.Many2one("sale.order", string="Devis / commande")

    kanban_color = fields.Integer(string="Couleur kanban", compute="_compute_kanban_color")
    is_open = fields.Boolean(string="Dossier ouvert", compute="_compute_is_open", search="_search_is_open")
    contact_warning = fields.Char(string="Alerte contact", compute="_compute_contact_warning")
    client_phone = fields.Char(string="Téléphone client", compute="_compute_client_contact")
    client_email = fields.Char(string="Email client", compute="_compute_client_contact")
    next_action = fields.Char(string="Prochaine action", compute="_compute_operational_indicators")
    blocking_reason = fields.Char(string="Point bloquant", compute="_compute_operational_indicators")
    days_since_deposit = fields.Integer(string="Jours depuis dépôt", compute="_compute_days_since_deposit")

    @api.model
    def _default_warehouse_id(self):
        warehouse = self.env["stock.warehouse"].search([("company_id", "=", self.env.company.id)], limit=1)
        return warehouse.id or False


    @api.model
    def _ensure_sequence_and_next(self):
        sequence = self.env["ir.sequence"].sudo().search([("code", "=", "sav.magasin.order")], limit=1)
        if not sequence:
            sequence = self.env["ir.sequence"].sudo().create({
                "name": "Dossier batterie Re-Watt ERP",
                "code": "sav.magasin.order",
                "prefix": "RW%(y)s",
                "padding": 5,
                "company_id": False,
            })
        return sequence.next_by_id() or "Nouveau"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = self.env["ir.sequence"].next_by_code("sav.magasin.order") or self._ensure_sequence_and_next()
            if vals.get("partner_id"):
                vals.setdefault("billing_partner_id", vals.get("partner_id"))
                vals.setdefault("delivered_partner_id", vals.get("partner_id"))
        orders = super().create(vals_list)
        for order in orders:
            order.message_post(body=_("Dossier batterie créé."))
        return orders

    @api.depends("part_line_ids.subtotal", "amount_labor")
    def _compute_amounts(self):
        for order in self:
            order.amount_parts = sum(order.part_line_ids.mapped("subtotal"))
            order.amount_total = order.amount_parts + order.amount_labor

    @api.depends("part_line_ids")
    def _compute_part_line_count(self):
        for order in self:
            order.part_line_count = len(order.part_line_ids)

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

    @api.depends("partner_id", "partner_id.phone", "partner_id.email")
    def _compute_client_contact(self):
        for order in self:
            order.client_phone = order.partner_id.phone or (order.partner_id["mobile"] if order.partner_id and "mobile" in order.partner_id._fields else False)
            order.client_email = order.partner_id.email

    @api.depends("state", "part_line_ids", "diagnosis", "repair_note", "invoice_id", "sale_order_id")
    def _compute_operational_indicators(self):
        for order in self:
            next_action = False
            blocking_reason = False
            if order.state == "draft":
                next_action = _("Compléter les champs obligatoires puis valider le dépôt.")
                missing = order._get_deposit_missing_fields()
                if missing:
                    blocking_reason = _("Dépôt incomplet : %s") % ", ".join(missing)
            elif order.state == "new":
                next_action = _("Lancer le diagnostic atelier.")
            elif order.state == "diagnosis":
                next_action = _("Compléter le diagnostic puis décider : attente client, attente composant batterie ou réparation.")
                if not order.diagnosis:
                    blocking_reason = _("Diagnostic non renseigné.")
            elif order.state == "customer_wait":
                next_action = _("Relancer le client ou saisir son accord.")
                blocking_reason = _("En attente d'une décision client.")
            elif order.state == "part_wait":
                next_action = _("Suivre les composants batterie attendues, transfert ou commande fournisseur.")
                blocking_reason = _("En attente de composant batterie.")
            elif order.state == "repair":
                next_action = _("Terminer l'intervention et renseigner le compte-rendu.")
                if not order.repair_note:
                    blocking_reason = _("Compte-rendu réparation non renseigné.")
            elif order.state == "ready":
                next_action = _("Facturer si nécessaire, prévenir le client et préparer la restitution.")
                if not order.invoice_id and not order.sale_order_id:
                    blocking_reason = _("Aucun devis, commande ou facture lié au dossier.")
            elif order.state == "invoiced":
                next_action = _("Restituer le produit au client.")
            elif order.state == "returned":
                next_action = _("Contrôler le dossier puis le clôturer.")
            elif order.state == "closed":
                next_action = _("Dossier terminé.")
            elif order.state == "cancelled":
                next_action = _("Dossier annulé. Remettre en brouillon si erreur.")
            order.next_action = next_action
            order.blocking_reason = blocking_reason

    @api.depends("deposit_date")
    def _compute_days_since_deposit(self):
        now = fields.Datetime.now()
        for order in self:
            if order.deposit_date:
                delta = now - order.deposit_date
                order.days_since_deposit = max(delta.days, 0)
            else:
                order.days_since_deposit = 0

    def _partner_has_minimum_contact(self, partner):
        mobile = partner["mobile"] if partner and "mobile" in partner._fields else False
        return bool(partner.phone or partner.email or mobile)

    def _get_deposit_missing_fields(self):
        self.ensure_one()
        missing = []
        if not self.partner_id:
            missing.append(_("Client"))
        elif not self._partner_has_minimum_contact(self.partner_id):
            missing.append(_("Téléphone ou email client"))
        if not self.device_name:
            missing.append(_("Batterie"))
        if not self.symptom:
            missing.append(_("Symptôme client"))
        if not self.visual_state:
            missing.append(_("État visuel"))
        if not self.warehouse_id:
            missing.append(_("Magasin"))
        return missing

    def _ensure_required_for_deposit(self):
        for order in self:
            missing = order._get_deposit_missing_fields()
            if missing:
                raise ValidationError(_("Impossible de valider le dépôt. Champs manquants : %s") % ", ".join(missing))

    def _ensure_state(self, allowed_states):
        for order in self:
            if order.state not in allowed_states:
                raise ValidationError(_("Action impossible depuis le statut actuel : %s") % dict(order._fields["state"].selection).get(order.state))

    def _set_state(self, state, message, extra_values=None):
        values = {"state": state}
        if extra_values:
            values.update(extra_values)
        self.write(values)
        for order in self:
            order.message_post(body=message)
        return True

    def action_validate_deposit(self):
        self._ensure_state(["draft"])
        self._ensure_required_for_deposit()
        return self._set_state("new", _("Dépôt validé."), {"deposit_validated_date": fields.Datetime.now()})

    def action_start_diagnosis(self):
        self._ensure_state(["new"])
        return self._set_state("diagnosis", _("Diagnostic lancé."), {"diagnosis_date": fields.Datetime.now()})

    def action_wait_customer(self):
        self._ensure_state(["diagnosis", "repair", "ready"])
        return self._set_state("customer_wait", _("Dossier mis en attente client."))

    def action_wait_part(self):
        self._ensure_state(["diagnosis", "repair"])
        return self._set_state("part_wait", _("Dossier mis en attente composant batterie."))

    def action_start_repair(self):
        self._ensure_state(["diagnosis", "customer_wait", "part_wait"])
        return self._set_state("repair", _("Réparation démarrée."), {"repair_start_date": fields.Datetime.now()})

    def action_ready(self):
        self._ensure_state(["repair"])
        return self._set_state("ready", _("Dossier prêt à restituer."), {"ready_date": fields.Datetime.now()})

    def action_mark_invoiced(self):
        self._ensure_state(["ready"])
        return self._set_state("invoiced", _("Dossier marqué comme facturé."))

    def action_returned(self):
        self._ensure_state(["ready", "invoiced"])
        self.write({"state": "returned", "return_date": fields.Datetime.now()})
        for order in self:
            order.message_post(body=_("Batterie restituée au client."))
        return True

    def action_close(self):
        self._ensure_state(["returned"])
        return self._set_state("closed", _("Dossier clôturé."), {"closed_date": fields.Datetime.now()})

    def action_cancel(self):
        self._ensure_state(["draft", "new", "diagnosis", "customer_wait", "part_wait", "repair", "ready", "invoiced"])
        return self._set_state("cancelled", _("Dossier annulé."))

    def action_reset_to_draft(self):
        self._ensure_state(["cancelled"])
        return self._set_state("draft", _("Dossier remis en brouillon."))

    def action_print_deposit(self):
        return self.env.ref("sav_magasin_core.action_report_sav_magasin_sav_deposit").report_action(self)

    def action_print_return(self):
        return self.env.ref("sav_magasin_core.action_report_sav_magasin_sav_return").report_action(self)

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
    _description = "Ligne composant batterie"
    _order = "order_id, sequence, id"

    sequence = fields.Integer(default=10)
    order_id = fields.Many2one("sav.magasin.order", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", string="Article / composant batterie", required=True)
    name = fields.Char(string="Description")
    quantity = fields.Float(default=1.0, required=True)
    price_unit = fields.Monetary(string="Prix unitaire")
    subtotal = fields.Monetary(compute="_compute_subtotal", store=True)
    currency_id = fields.Many2one(related="order_id.currency_id", readonly=True)
    state = fields.Selection(
        [
            ("to_check", "À vérifier"),
            ("reserved", "Réservée"),
            ("consumed", "Consommée"),
            ("cancelled", "Annulée"),
        ],
        string="Statut ligne",
        default="to_check",
    )
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
                raise ValidationError(_("La quantité de composant batterie doit être supérieure à zéro."))

    @api.depends("quantity", "price_unit")
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    def action_mark_reserved(self):
        self.write({"state": "reserved"})
        return True

    def action_mark_consumed(self):
        self.write({"state": "consumed"})
        return True

    def action_cancel_line(self):
        self.write({"state": "cancelled"})
        return True
