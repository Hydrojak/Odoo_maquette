from . import models
from . import wizard


def _upsert(env, model, domain, values):
    Model = env[model].sudo()
    record = Model.search(domain, limit=1)
    if record:
        record.write(values)
        return record
    return Model.create(values)


def post_init_hook(env):
    """Create default battery checklist templates without XML data files."""
    template = _upsert(
        env,
        "sav.battery.checklist.template",
        [("code", "=", "BATTERY_QC_V1")],
        {
            "name": "Checklist batterie < 60 V - Standard atelier",
            "code": "BATTERY_QC_V1",
            "version": "1.0",
            "active": True,
            "description": "Contrôles de base issus du workflow Atway/Re-Watt : identification, préparation, assemblage, BMS, charge/décharge et validation finale.",
        },
    )

    controls = [
        {
            "phase": "identification", "sequence": 10, "name": "Commande identifiée",
            "expected": "N° commande / dossier rattaché à la batterie", "type": "text", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": False, "note": "Scanner ou saisir le numéro de dossier/commande avant tout contrôle."
        },
        {
            "phase": "identification", "sequence": 20, "name": "Tension maximale < 60 V",
            "expected": "La tension maximale mesurée ou déclarée doit rester strictement inférieure à 60 V", "type": "numeric", "unit": "V",
            "use_min": False, "min": 0, "use_max": True, "max": 59.99, "required": True, "blocking": True,
            "photo_fail": True, "note": "Toute valeur ≥ 60 V bloque le workflow standard Re-Watt."
        },
        {
            "phase": "diagnosis", "sequence": 30, "name": "Aspect visuel cellules",
            "expected": "Gaine/wrap intact, pas d’impact ni trace d’échauffement", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": True, "note": "Ajouter une photo si gaine abîmée, choc, gonflement ou échauffement."
        },
        {
            "phase": "cell_preparation", "sequence": 40, "name": "Delta cellules avant assemblage",
            "expected": "Écart maximal entre cellules ≤ 0,05 V", "type": "numeric", "unit": "V",
            "use_min": False, "min": 0, "use_max": True, "max": 0.05, "required": True, "blocking": True,
            "photo_fail": True, "note": "Saisir le delta maximal mesuré entre cellules."
        },
        {
            "phase": "cell_preparation", "sequence": 50, "name": "Isolants œillets présents",
            "expected": "Isolants présents sur les cellules concernées", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": True, "note": "Contrôler avant soudure."
        },
        {
            "phase": "assembly", "sequence": 60, "name": "Sens cellules conforme notice",
            "expected": "Orientation conforme à la notice de montage applicable", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": True, "note": "Renseigner la version de notice sur le dossier batterie."
        },
        {
            "phase": "assembly", "sequence": 70, "name": "Nickel conforme notice",
            "expected": "Référence et positionnement du nickel conformes à la notice", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": False,
            "photo_fail": True, "note": "Contrôler matière, largeur et positionnement."
        },
        {
            "phase": "welding", "sequence": 80, "name": "Nombre de points de soudure",
            "expected": "Nombre de points conforme au standard atelier", "type": "numeric", "unit": "points",
            "use_min": True, "min": 6, "use_max": False, "max": 0, "required": True, "blocking": False,
            "photo_fail": True, "note": "Par défaut : minimum 6 points. Adapter le modèle si la notice indique une autre valeur."
        },
        {
            "phase": "welding", "sequence": 90, "name": "Solidité points de soudure",
            "expected": "Pas de claquement, point stable au contrôle atelier", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": True, "note": "Définir le mode opératoire atelier : traction légère / contrôle visuel."
        },
        {
            "phase": "welding", "sequence": 95, "name": "Isolement Kapton / papier isolant",
            "expected": "Présence de Kapton et papier isolant aux emplacements requis", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": True, "note": "Contrôle visuel obligatoire avant fermeture pack."
        },
        {
            "phase": "bms", "sequence": 100, "name": "Contrôle BMS",
            "expected": "BMS correctement raccordé, isolé et fonctionnel", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": True, "note": "Contrôler câblage, fixation, isolement et protection."
        },
        {
            "phase": "charge", "sequence": 110, "name": "Tension connectique avant charge",
            "expected": "Tension cohérente entre B+ / P- et connectique", "type": "numeric", "unit": "V",
            "use_min": False, "min": 0, "use_max": True, "max": 59.99, "required": True, "blocking": False,
            "photo_fail": False, "note": "Saisir la tension réellement mesurée à la connectique."
        },
        {
            "phase": "charge", "sequence": 120, "name": "Équilibrage fin de charge",
            "expected": "Delta cellules en fin de charge ≤ 0,05 V", "type": "numeric", "unit": "V",
            "use_min": False, "min": 0, "use_max": True, "max": 0.05, "required": True, "blocking": True,
            "photo_fail": True, "note": "Saisir le delta maximal constaté en fin de charge."
        },
        {
            "phase": "discharge", "sequence": 130, "name": "Température BMS en décharge",
            "expected": "Température BMS < 60 °C", "type": "numeric", "unit": "°C",
            "use_min": False, "min": 0, "use_max": True, "max": 59.99, "required": True, "blocking": True,
            "photo_fail": True, "note": "Mesure chiffrée obligatoire pendant ou juste après le test décharge."
        },
        {
            "phase": "discharge", "sequence": 140, "name": "Équilibrage après décharge",
            "expected": "Différence maximale entre cellules ≤ 0,05 V", "type": "numeric", "unit": "V",
            "use_min": False, "min": 0, "use_max": True, "max": 0.05, "required": True, "blocking": True,
            "photo_fail": True, "note": "Saisir le delta maximal après décharge."
        },
        {
            "phase": "final_validation", "sequence": 150, "name": "Validation finale technicien",
            "expected": "Batterie conforme, dossier prêt pour rapport technicien", "type": "boolean", "unit": "",
            "use_min": False, "min": 0, "use_max": False, "max": 0, "required": True, "blocking": True,
            "photo_fail": False, "note": "Dernière validation avant rapport technicien."
        },
    ]

    Line = env["sav.battery.checklist.template.line"].sudo()
    for control in controls:
        existing = Line.search([("template_id", "=", template.id), ("sequence", "=", control["sequence"]), ("name", "=", control["name"])], limit=1)
        values = {
            "template_id": template.id,
            "phase": control["phase"],
            "sequence": control["sequence"],
            "name": control["name"],
            "expected_criteria": control["expected"],
            "measurement_type": control["type"],
            "unit": control["unit"],
            "use_min_value": control["use_min"],
            "min_value": control["min"],
            "use_max_value": control["use_max"],
            "max_value": control["max"],
            "required": control["required"],
            "blocking": control["blocking"],
            "requires_photo_on_fail": control["photo_fail"],
            "note": control["note"],
        }
        if existing:
            existing.write(values)
        else:
            Line.create(values)

    # Add one sample battery model if the demo project is installed later or absent.
    _upsert(
        env,
        "sav.battery.model",
        [("name", "=", "Pack batterie atelier 36 V 10 Ah")],
        {
            "name": "Pack batterie atelier 36 V 10 Ah",
            "nominal_voltage": 36.0,
            "max_voltage": 42.0,
            "capacity_ah": 10.0,
            "chemistry": "li_ion",
            "series_count": 10,
            "parallel_count": 4,
            "bms_type": "BMS 10S standard",
            "connector_type": "XT60",
            "charger_voltage": 42.0,
            "active": True,
        },
    )
