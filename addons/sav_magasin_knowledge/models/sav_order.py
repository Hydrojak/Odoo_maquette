from odoo import _, fields, models


class SavMagasinOrderKnowledge(models.Model):
    _inherit = "sav.magasin.order"

    help_procedure_count = fields.Integer(string="Procédures", compute="_compute_help_procedure_count")

    def _compute_help_procedure_count(self):
        Procedure = self.env["sav.magasin.procedure"]
        for order in self:
            domain = order._get_contextual_procedure_domain()
            order.help_procedure_count = Procedure.search_count(domain)

    def _get_contextual_procedure_domain(self):
        self.ensure_one()
        domain = [("active", "=", True)]
        if self.state:
            domain += ["|", ("applicable_state", "=", False), ("applicable_state", "=", self.state)]
        return domain

    def action_open_contextual_procedures(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Procédures métier"),
            "res_model": "sav.magasin.procedure",
            "view_mode": "list,form",
            "domain": self._get_contextual_procedure_domain(),
            "context": {"default_applicable_state": self.state},
            "target": "current",
        }
