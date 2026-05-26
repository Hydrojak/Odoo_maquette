"""Demo records for Re-Watt ERP created through ORM.

The demo dataset is now battery-focused: batteries < 60 V, BMS, cells,
nickel, Kapton, connectors and workshop checklists.
"""


def _get_or_create(env, model, domain, vals):
    Model = env[model].sudo()
    record = Model.search(domain, limit=1)
    if record:
        record.write(vals)
        return record
    return Model.create(vals)


def _product_variant(template):
    return template.product_variant_id


def post_init_hook(env):
    brand_rewatt = _get_or_create(env, "sav.magasin.product.brand", [("name", "=", "Re-Watt")], {
        "name": "Re-Watt",
        "note": "Marque atelier utilisée pour les packs batterie de démonstration.",
    })
    brand_cells = _get_or_create(env, "sav.magasin.product.brand", [("name", "=", "Cellules génériques")], {
        "name": "Cellules génériques",
        "note": "Famille de composants batterie : cellules lithium et accessoires.",
    })
    brand_bms = _get_or_create(env, "sav.magasin.product.brand", [("name", "=", "BMS Atelier")], {
        "name": "BMS Atelier",
        "note": "Famille de composants BMS pour démonstration.",
    })

    range_36v = _get_or_create(env, "sav.magasin.product.range", [("name", "=", "Pack 36 V"), ("brand_id", "=", brand_rewatt.id)], {
        "name": "Pack 36 V",
        "brand_id": brand_rewatt.id,
    })
    range_48v = _get_or_create(env, "sav.magasin.product.range", [("name", "=", "Pack 48 V"), ("brand_id", "=", brand_rewatt.id)], {
        "name": "Pack 48 V",
        "brand_id": brand_rewatt.id,
    })
    range_components = _get_or_create(env, "sav.magasin.product.range", [("name", "=", "Composants batterie"), ("brand_id", "=", brand_cells.id)], {
        "name": "Composants batterie",
        "brand_id": brand_cells.id,
    })

    model_10s4p = _get_or_create(env, "sav.magasin.device.model", [("name", "=", "Pack batterie 10S4P 36 V")], {
        "name": "Pack batterie 10S4P 36 V",
        "brand_id": brand_rewatt.id,
        "range_id": range_36v.id,
    })
    model_13s5p = _get_or_create(env, "sav.magasin.device.model", [("name", "=", "Pack batterie 13S5P 48 V")], {
        "name": "Pack batterie 13S5P 48 V",
        "brand_id": brand_rewatt.id,
        "range_id": range_48v.id,
    })

    article_type_component = _get_or_create(env, "sav.magasin.article.type", [("code", "=", "BAT_COMP")], {
        "sequence": 10,
        "name": "Composant batterie",
        "code": "BAT_COMP",
        "stock_managed": True,
    })
    article_type_service = _get_or_create(env, "sav.magasin.article.type", [("code", "=", "BAT_SERVICE")], {
        "sequence": 20,
        "name": "Prestation atelier batterie",
        "code": "BAT_SERVICE",
        "stock_managed": False,
    })
    article_type_consumable = _get_or_create(env, "sav.magasin.article.type", [("code", "=", "BAT_CONSO")], {
        "sequence": 30,
        "name": "Consommable atelier batterie",
        "code": "BAT_CONSO",
        "stock_managed": True,
    })

    partner_client = _get_or_create(env, "res.partner", [("email", "=", "atelier.demo.client@example.com")], {
        "name": "Client Démo Re-Watt",
        "customer_rank": 1,
        "phone": "06 10 20 30 40",
        "email": "atelier.demo.client@example.com",
        "street": "12 rue de l'Énergie",
        "zip": "75011",
        "city": "Paris",
        "sav_magasin_customer_type": "b2c",
        "sav_magasin_internal_note": "Client de démonstration : dépôt d'une batterie < 60 V.",
    })
    partner_b2b = _get_or_create(env, "res.partner", [("email", "=", "maintenance@cycle-pro.example.com")], {
        "name": "Cycle Pro Maintenance",
        "is_company": True,
        "customer_rank": 1,
        "phone": "01 44 00 00 48",
        "email": "maintenance@cycle-pro.example.com",
        "street": "8 avenue des Mobilités",
        "zip": "69003",
        "city": "Lyon",
        "sav_magasin_customer_type": "b2b",
        "sav_magasin_internal_note": "Client professionnel de démonstration : batteries de flotte < 60 V.",
    })
    supplier = _get_or_create(env, "res.partner", [("email", "=", "supply@battery-components.example.com")], {
        "name": "Battery Components Supply",
        "is_company": True,
        "supplier_rank": 1,
        "phone": "01 80 60 00 40",
        "email": "supply@battery-components.example.com",
        "street": "5 zone logistique énergie",
        "zip": "93200",
        "city": "Saint-Denis",
    })

    def product_template(name, vals):
        defaults = {
            "name": name,
            "list_price": vals.pop("list_price", 0.0),
            "standard_price": vals.pop("standard_price", 0.0),
        }
        defaults.update(vals)
        return _get_or_create(env, "product.template", [("name", "=", name)], defaults)

    tmpl_cell = product_template("Cellule lithium 18650 3,6 V 3 Ah", {
        "list_price": 7.5,
        "standard_price": 3.2,
        "sav_magasin_brand_id": brand_cells.id,
        "sav_magasin_range_id": range_components.id,
        "sav_magasin_article_type_id": article_type_component.id,
        "sav_magasin_supplier_reference": "CELL-18650-3AH",
        "sav_magasin_location_hint": "Stock cellules / Bac C01",
    })
    tmpl_bms_10s = product_template("BMS 10S 36 V 20 A", {
        "list_price": 39.0,
        "standard_price": 18.0,
        "sav_magasin_brand_id": brand_bms.id,
        "sav_magasin_article_type_id": article_type_component.id,
        "sav_magasin_supplier_reference": "BMS-10S-20A",
        "sav_magasin_location_hint": "Stock BMS / Bac B10",
    })
    tmpl_bms_13s = product_template("BMS 13S 48 V 25 A", {
        "list_price": 49.0,
        "standard_price": 24.0,
        "sav_magasin_brand_id": brand_bms.id,
        "sav_magasin_article_type_id": article_type_component.id,
        "sav_magasin_supplier_reference": "BMS-13S-25A",
        "sav_magasin_location_hint": "Stock BMS / Bac B13",
    })
    tmpl_nickel = product_template("Bande nickel pur 0,15 mm", {
        "list_price": 12.0,
        "standard_price": 4.0,
        "sav_magasin_article_type_id": article_type_consumable.id,
        "sav_magasin_location_hint": "Consommables / Nickel",
    })
    tmpl_kapton = product_template("Ruban Kapton 20 mm", {
        "list_price": 8.0,
        "standard_price": 2.0,
        "sav_magasin_article_type_id": article_type_consumable.id,
        "sav_magasin_location_hint": "Consommables / Isolation",
    })
    tmpl_xt60 = product_template("Connecteur XT60", {
        "list_price": 4.5,
        "standard_price": 1.2,
        "sav_magasin_article_type_id": article_type_component.id,
        "sav_magasin_location_hint": "Connectique / XT",
    })
    tmpl_labor = product_template("Diagnostic batterie atelier", {
        "list_price": 49.0,
        "standard_price": 0.0,
        "sav_magasin_article_type_id": article_type_service.id,
    })

    product_cell = _product_variant(tmpl_cell)
    product_bms_10s = _product_variant(tmpl_bms_10s)
    product_bms_13s = _product_variant(tmpl_bms_13s)
    product_nickel = _product_variant(tmpl_nickel)
    product_kapton = _product_variant(tmpl_kapton)
    product_xt60 = _product_variant(tmpl_xt60)
    product_labor = _product_variant(tmpl_labor)

    if "sav.magasin.product.substitution" in env.registry:
        _get_or_create(env, "sav.magasin.product.substitution", [
            ("original_product_id", "=", product_bms_10s.id),
            ("substitute_product_id", "=", product_bms_13s.id),
        ], {
            "original_product_id": product_bms_10s.id,
            "substitute_product_id": product_bms_13s.id,
            "substitution_type": "compatible",
            "validation_state": "to_test",
            "priority": 20,
            "warranty_impact": "confirm",
            "technical_note": "Substitution à valider selon architecture et intensité admissible.",
        })

    battery_model_36 = None
    battery_model_48 = None
    if "sav.battery.model" in env.registry:
        battery_model_36 = _get_or_create(env, "sav.battery.model", [("name", "=", "Pack 36 V 10S4P - Démo")], {
            "name": "Pack 36 V 10S4P - Démo",
            "nominal_voltage": 36.0,
            "max_voltage": 42.0,
            "capacity_ah": 12.0,
            "chemistry": "li_ion",
            "series_count": 10,
            "parallel_count": 4,
            "bms_type": "BMS 10S 20 A",
            "connector_type": "XT60",
            "charger_voltage": 42.0,
        })
        battery_model_48 = _get_or_create(env, "sav.battery.model", [("name", "=", "Pack 48 V 13S5P - Démo")], {
            "name": "Pack 48 V 13S5P - Démo",
            "nominal_voltage": 48.0,
            "max_voltage": 54.6,
            "capacity_ah": 15.0,
            "chemistry": "li_ion",
            "series_count": 13,
            "parallel_count": 5,
            "bms_type": "BMS 13S 25 A",
            "connector_type": "XT90",
            "charger_voltage": 54.6,
        })

    warehouse = env["stock.warehouse"].sudo().search([("company_id", "=", env.company.id)], limit=1)
    order_values = [
        {
            "name": "RW-DEMO-001",
            "partner_id": partner_client.id,
            "warehouse_id": warehouse.id if warehouse else False,
            "device_name": "Pack batterie 36 V 10S4P",
            "brand_id": brand_rewatt.id,
            "range_id": range_36v.id,
            "model_id": model_10s4p.id,
            "serial_number": "BAT-36V-DEMO-001",
            "warranty_state": "unknown",
            "symptom": "Autonomie faible et coupure sous charge.",
            "visual_state": "Pack intact, gaine externe marquée, aucune trace de brûlure visible.",
            "accessories": "Chargeur 42 V fourni.",
            "state": "diagnosis",
            "diagnosis": "Diagnostic initial en cours : contrôle tension cellules et BMS.",
            "is_battery_repair": True,
            "battery_model_id": battery_model_36.id if battery_model_36 else False,
            "battery_serial": "BAT-36V-DEMO-001",
            "battery_nominal_voltage": 36.0,
            "battery_max_voltage": 42.0,
            "battery_capacity_ah": 12.0,
            "battery_chemistry": "li_ion",
            "battery_series_count": 10,
            "battery_parallel_count": 4,
            "bms_type": "BMS 10S 20 A",
            "connector_type": "XT60",
            "charger_voltage": 42.0,
            "battery_stage": "diagnosis",
        },
        {
            "name": "RW-DEMO-002",
            "partner_id": partner_b2b.id,
            "warehouse_id": warehouse.id if warehouse else False,
            "device_name": "Pack batterie 48 V 13S5P",
            "brand_id": brand_rewatt.id,
            "range_id": range_48v.id,
            "model_id": model_13s5p.id,
            "serial_number": "BAT-48V-DEMO-002",
            "warranty_state": "out_warranty",
            "symptom": "BMS coupe à l'accélération ; suspicion déséquilibrage cellules.",
            "visual_state": "Pack propre, connectique XT90 à vérifier.",
            "accessories": "Chargeur 54,6 V fourni.",
            "state": "testing",
            "diagnosis": "Pack assemblé, passage en test charge/décharge.",
            "is_battery_repair": True,
            "battery_model_id": battery_model_48.id if battery_model_48 else False,
            "battery_serial": "BAT-48V-DEMO-002",
            "battery_nominal_voltage": 48.0,
            "battery_max_voltage": 54.6,
            "battery_capacity_ah": 15.0,
            "battery_chemistry": "li_ion",
            "battery_series_count": 13,
            "battery_parallel_count": 5,
            "bms_type": "BMS 13S 25 A",
            "connector_type": "XT90",
            "charger_voltage": 54.6,
            "battery_stage": "testing",
        },
        {
            "name": "RW-DEMO-003",
            "partner_id": partner_client.id,
            "warehouse_id": warehouse.id if warehouse else False,
            "device_name": "Pack batterie 36 V en attente BMS",
            "brand_id": brand_rewatt.id,
            "range_id": range_36v.id,
            "model_id": model_10s4p.id,
            "serial_number": "BAT-36V-DEMO-003",
            "warranty_state": "out_warranty",
            "symptom": "BMS absent après démontage, commande composant nécessaire.",
            "visual_state": "Cellules visuellement correctes, isolation à reprendre.",
            "accessories": "Sans chargeur.",
            "state": "part_wait",
            "diagnosis": "BMS 10S à commander avant assemblage final.",
            "is_battery_repair": True,
            "battery_model_id": battery_model_36.id if battery_model_36 else False,
            "battery_serial": "BAT-36V-DEMO-003",
            "battery_nominal_voltage": 36.0,
            "battery_max_voltage": 42.0,
            "battery_capacity_ah": 10.0,
            "battery_chemistry": "li_ion",
            "battery_series_count": 10,
            "battery_parallel_count": 4,
            "bms_type": "BMS 10S 20 A",
            "connector_type": "XT60",
            "charger_voltage": 42.0,
            "battery_stage": "repair_in_progress",
        },
    ]
    orders = {}
    for vals in order_values:
        orders[vals["name"]] = _get_or_create(env, "sav.magasin.order", [("name", "=", vals["name"])], vals)

    PartLine = env["sav.magasin.part.line"].sudo()
    parts_to_add = [
        ("RW-DEMO-001", product_labor, 1, 49.0, "Diagnostic batterie atelier."),
        ("RW-DEMO-001", product_kapton, 1, 8.0, "Isolation Kapton à contrôler."),
        ("RW-DEMO-002", product_nickel, 1, 12.0, "Nickel consommé pour reprise assemblage."),
        ("RW-DEMO-002", product_xt60, 1, 4.5, "Connectique à contrôler / remplacer si nécessaire."),
        ("RW-DEMO-003", product_bms_10s, 1, 39.0, "BMS à commander pour reprise du dossier."),
        ("RW-DEMO-003", product_cell, 4, 7.5, "Cellules de remplacement potentielles."),
    ]
    for order_name, product, qty, price, note in parts_to_add:
        if not PartLine.search([("order_id", "=", orders[order_name].id), ("product_id", "=", product.id)], limit=1):
            PartLine.create({
                "order_id": orders[order_name].id,
                "product_id": product.id,
                "quantity": qty,
                "price_unit": price,
                "state": "purchase_needed" if "commander" in note else "to_check",
                "note": note,
            })

    if "sav.magasin.quick.receipt" in env.registry and warehouse:
        receipt = _get_or_create(env, "sav.magasin.quick.receipt", [("name", "=", "REC-RW-DEMO-001")], {
            "name": "REC-RW-DEMO-001",
            "partner_id": supplier.id,
            "warehouse_id": warehouse.id,
            "delivery_note": "BL-BAT-DEMO-001",
            "vendor_bill_ref": "FAC-BAT-DEMO-001",
            "sav_order_id": orders["RW-DEMO-003"].id,
            "note": "Réception de démonstration liée à un dossier batterie en attente BMS.",
        })
        if not receipt.line_ids:
            part_line = PartLine.search([("order_id", "=", orders["RW-DEMO-003"].id), ("product_id", "=", product_bms_10s.id)], limit=1)
            env["sav.magasin.quick.receipt.line"].sudo().create({
                "receipt_id": receipt.id,
                "product_id": product_bms_10s.id,
                "quantity": 1,
                "price_unit": 18.0,
                "location_hint": "Stock BMS / Bac B10",
                "sav_part_line_id": part_line.id,
            })

    if "sav.battery.checklist" in env.registry and "sav.battery.checklist.template" in env.registry:
        template = env["sav.battery.checklist.template"].sudo().search([("active", "=", True)], limit=1)
        if template:
            order = orders["RW-DEMO-001"]
            if not env["sav.battery.checklist"].sudo().search([("repair_id", "=", order.id)], limit=1):
                checklist = env["sav.battery.checklist"].sudo().create_from_template(order, template)
                for line in checklist.line_ids[:3]:
                    line.write({"verdict": "pass", "comment": "Contrôle conforme pour démonstration."})
    if "sav.battery.diagnostic" in env.registry:
        _get_or_create(env, "sav.battery.diagnostic", [
            ("repair_id", "=", orders["RW-DEMO-002"].id),
            ("cause", "=", "charge_discharge_issue"),
            ("state", "=", "open"),
        ], {
            "repair_id": orders["RW-DEMO-002"].id,
            "severity": "critical",
            "cause": "charge_discharge_issue",
            "description": "Diagnostic de démonstration : température BMS et équilibrage à confirmer pendant le test décharge.",
            "corrective_action": "Contrôler la température BMS sous charge, vérifier équilibrage cellules, documenter la mesure finale.",
            "responsible_id": env.user.id,
            "state": "open",
        })

    if "sav.battery.test.session" in env.registry:
        TestSession = env["sav.battery.test.session"].sudo()
        TestMeasurement = env["sav.battery.test.measurement"].sudo()
        order = orders["RW-DEMO-002"]
        session = _get_or_create(env, "sav.battery.test.session", [
            ("repair_id", "=", order.id),
            ("test_type", "=", "discharge"),
        ], {
            "repair_id": order.id,
            "test_type": "discharge",
            "operator_id": env.user.id,
            "state": "done",
            "note": "Session de démonstration : température BMS et delta cellules à surveiller.",
        })
        if not session.measurement_ids:
            TestMeasurement.create({
                "session_id": session.id,
                "sequence": 10,
                "name": "Début décharge",
                "voltage_start": 54.1,
                "voltage_end": 53.4,
                "current_a": 8.0,
                "capacity_ah": 2.0,
                "temperature_c": 42.0,
                "cell_delta_v": 0.03,
                "comment": "Début de test conforme.",
            })
            TestMeasurement.create({
                "session_id": session.id,
                "sequence": 20,
                "name": "Fin décharge",
                "voltage_start": 53.4,
                "voltage_end": 47.8,
                "current_a": 12.0,
                "capacity_ah": 12.2,
                "temperature_c": 61.5,
                "cell_delta_v": 0.07,
                "comment": "Température BMS et delta cellules hors seuil pour démonstration.",
            })

