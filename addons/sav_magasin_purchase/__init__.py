from . import models


def post_init_hook(env):
    """Create required sequences through ORM to avoid XML-data validation issues."""
    Sequence = env["ir.sequence"].sudo()
    if not Sequence.search([("code", "=", "sav.magasin.quick.receipt")], limit=1):
        Sequence.create({
            "name": "Réception sans commande batterie",
            "code": "sav.magasin.quick.receipt",
            "prefix": "REC%(y)s",
            "padding": 5,
            "company_id": False,
        })
