from . import models
from . import wizard


def post_init_hook(env):
    """Create required sequences through ORM to avoid XML-data validation issues."""
    Sequence = env["ir.sequence"].sudo()
    if not Sequence.search([("code", "=", "sav.magasin.order")], limit=1):
        Sequence.create({
            "name": "Dossier batterie Re-Watt ERP",
            "code": "sav.magasin.order",
            "prefix": "RW%(y)s",
            "padding": 5,
            "company_id": False,
        })
