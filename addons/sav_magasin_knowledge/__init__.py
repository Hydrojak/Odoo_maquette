from . import models


def _upsert(env, model, domain, values):
    Model = env[model].sudo()
    record = Model.search(domain, limit=1)
    if record:
        record.write(values)
        return record
    return Model.create(values)


def post_init_hook(env):
    """Create default battery-workshop procedures with ORM instead of XML data files."""
    procedures = [
        {
            "sequence": 10,
            "name": "Créer un dossier batterie < 60 V",
            "code": "CREATE_BATTERY_ORDER",
            "category": "comptoir",
            "role": "accueil",
            "applicable_state": "draft",
            "summary": "Procédure de prise en charge d'une batterie au comptoir atelier.",
            "content": """
                <ol>
                    <li>Rechercher ou créer le client.</li>
                    <li>Saisir le modèle batterie, le numéro de série, la tension nominale et la tension maximale.</li>
                    <li>Vérifier que la tension maximale est strictement inférieure à 60 V.</li>
                    <li>Saisir le symptôme, les accessoires, l'état visuel et la connectique.</li>
                    <li>Valider le dépôt uniquement si le dossier est complet.</li>
                </ol>
            """,
            "risk_note": "Risque majeur : accepter une batterie >= 60 V dans le workflow standard. Le blocage serveur du module batterie empêche cette validation.",
        },
        {
            "sequence": 20,
            "name": "Traiter une batterie en attente composant",
            "code": "BATTERY_PART_WAIT",
            "category": "stock",
            "role": "stock",
            "applicable_state": "part_wait",
            "summary": "Procédure de décision stock pour cellules, BMS, nickel, Kapton et connecteurs.",
            "content": """
                <ol>
                    <li>Identifier le composant demandé dans l'onglet Composants / stock.</li>
                    <li>Vérifier le stock local et distant.</li>
                    <li>Vérifier les substitutions validées ou à tester.</li>
                    <li>Créer une commande fournisseur si aucun composant compatible n'est disponible.</li>
                    <li>Rattacher la réception au dossier batterie.</li>
                </ol>
            """,
            "risk_note": "Ne pas utiliser un substitut BMS ou cellule sans validation technique atelier.",
        },
        {
            "sequence": 30,
            "name": "Exécuter la checklist qualité batterie",
            "code": "BATTERY_CHECKLIST",
            "category": "diagnostic",
            "role": "technician",
            "applicable_state": "diagnosis",
            "summary": "Contrôle qualité batterie : identification, préparation, assemblage, BMS, charge/décharge.",
            "content": """
                <ol>
                    <li>Créer une checklist depuis le dossier batterie.</li>
                    <li>Renseigner chaque contrôle obligatoire avec un verdict Conforme, Non conforme ou Non applicable.</li>
                    <li>Saisir les valeurs mesurées avec unité pour les contrôles chiffrés.</li>
                    <li>Ajouter un commentaire pour toute non-conformité.</li>
                    <li>Valider la checklist uniquement lorsque tous les contrôles obligatoires sont complétés.</li>
                </ol>
            """,
            "risk_note": "Un contrôle bloquant non conforme doit rester traçable et empêcher la validation finale.",
        },
    ]

    for values in procedures:
        procedure = _upsert(env, "sav.magasin.procedure", [("code", "=", values["code"])], values)
        if not procedure.step_ids:
            env["sav.magasin.procedure.step"].sudo().create({
                "procedure_id": procedure.id,
                "sequence": 10,
                "name": "Appliquer la procédure",
                "description": values["summary"],
                "expected_result": "Action tracée dans le dossier batterie.",
            })

    faqs = [
        {
            "question": "Pourquoi bloquer les batteries >= 60 V ?",
            "answer": "<p>Le périmètre atelier Re-Watt concerne uniquement les batteries strictement inférieures à 60 V. La contrainte est appliquée côté serveur Odoo.</p>",
            "category": "comptoir",
        },
        {
            "question": "Que faire si une mesure de checklist est hors seuil ?",
            "answer": "<p>Le contrôle passe en non conforme. Un commentaire est obligatoire, et les prochaines versions lieront automatiquement la non-conformité à un diagnostic batterie.</p>",
            "category": "diagnostic",
        },
    ]

    for values in faqs:
        _upsert(env, "sav.magasin.faq", [("question", "=", values["question"])], values)
