from odoo import fields, models


SAV_STATE_SELECTION = [
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
]


class SavMagasinProcedure(models.Model):
    _name = "sav.magasin.procedure"
    _description = "Procédure métier atelier batterie"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "sequence, name"

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    name = fields.Char(required=True, tracking=True)
    code = fields.Char(string="Code procédure")
    category = fields.Selection(
        [
            ("comptoir", "Atelier batteries"),
            ("diagnostic", "Diagnostic"),
            ("stock", "Stock / composants batterie"),
            ("substitution", "Substitution"),
            ("purchase", "Achat / réception"),
            ("return", "Restitution"),
            ("admin", "Administration"),
        ],
        string="Catégorie",
        default="comptoir",
        required=True,
    )
    role = fields.Selection(
        [
            ("accueil", "Accueil magasin"),
            ("technician", "Technicien batterie"),
            ("stock", "Stock / achats"),
            ("manager", "Responsable"),
            ("admin", "Administrateur métier"),
        ],
        string="Profil cible",
    )
    applicable_state = fields.Selection(SAV_STATE_SELECTION, string="Statut dossier concerné")
    summary = fields.Text(string="Résumé")
    content = fields.Html(string="Procédure détaillée")
    step_ids = fields.One2many("sav.magasin.procedure.step", "procedure_id", string="Étapes")
    risk_note = fields.Text(string="Risques / vigilance")
    question_note = fields.Text(string="Questions à confirmer")


class SavMagasinProcedureStep(models.Model):
    _name = "sav.magasin.procedure.step"
    _description = "Étape de procédure atelier batterie"
    _order = "procedure_id, sequence, id"

    procedure_id = fields.Many2one("sav.magasin.procedure", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    name = fields.Char(string="Étape", required=True)
    description = fields.Text(string="Description")
    expected_result = fields.Text(string="Résultat attendu")


class SavMagasinFaq(models.Model):
    _name = "sav.magasin.faq"
    _description = "FAQ métier atelier batterie"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    question = fields.Char(required=True)
    answer = fields.Html(required=True)
    category = fields.Selection(
        [
            ("comptoir", "Atelier batteries"),
            ("diagnostic", "Diagnostic batterie"),
            ("stock", "Stock / composants batterie"),
            ("substitution", "Substitution"),
            ("purchase", "Achat / réception"),
            ("return", "Restitution"),
            ("admin", "Administration"),
        ],
        default="comptoir",
        required=True,
    )
