from flask_restx import Namespace, Resource
from flask import jsonify

# Definizione del namespace per l'inventario
inventory_ns = Namespace('inventory', description='Network Hardware Inventory')

class InventoryAPI(Resource):
    def get(self):
        # Il JSON statico che vogliamo restituire come dizionario Python
        inventory_json = {
            "ietf-network-hardware-inventory:network-hardware-inventory": {
                "network-elements": {
                    "network-element": [
                        {
                            "name": "OLT",
                            "uuid": "olt-uuid-001",
                            "components": {
                                "component": [
                                    {
                                        "class": "olt",
                                        "name": "OLT",
                                        "description": "Optical Line Terminal",
                                        "uuid": "olt-uuid-001",
                                        "attributes": {
                                            "port": "xp1"
                                        },
                                        "child-components": [
                                            "pon-xp1-uuid"
                                        ]
                                    },
                                    {
                                        "class": "port",
                                        "name": "xp1",
                                        "description": "Passive Optical Network port",
                                        "uuid": "pon-xp1-uuid",
                                        "parent-component": "olt-uuid-001",
                                        "attributes": {
                                            "admin-state": "up",
                                            "oper-state": "up",
                                            "mac-address": "cc:be:59:4d:8b:80",
                                            "rx-pkts": 3303,
                                            "tx-pkts": 6053,
                                            "rx-octets": 329134,
                                            "tx-octets": 623343,
                                            "rx-errors": 0,
                                            "tx-errors": 0,
                                            "rx-fec-corrected": 150,
                                            "rx-fec-uncorrected": 41
                                        },
                                        "child-components": [
                                            "onu-uuid-001"
                                        ]
                                    },
                                    {
                                        "class": "port",
                                        "name": "xp2",
                                        "description": "Passive Optical Network port",
                                        "uuid": "pon-xp2-uuid",
                                        "parent-component": "olt-uuid-001",
                                        "attributes": {
                                            "admin-state": "up",
                                            "oper-state": "up",
                                            "mac-address": "cc:be:59:4d:8b:81",
                                            "rx-pkts": 3303,
                                            "tx-pkts": 6053,
                                            "rx-octets": 329134,
                                            "tx-octets": 623343,
                                            "rx-errors": 0,
                                            "tx-errors": 0,
                                            "rx-fec-corrected": 150,
                                            "rx-fec-uncorrected": 41
                                        },
                                        "child-components": [
                                            "onu-uuid-002"
                                        ]
                                    },
                                    {
                                        "class": "ont",
                                        "name": "ONT-1",
                                        "description": "Optical Network Terminal",
                                        "uuid": "ont-uuid-001",
                                        "parent-component": "pon-xp1-uuid",
                                        "attributes": {
                                            "vendor": "CXNK",
                                            "serial": "47846E",
                                            "product-code": "P8",
                                            "oper-state": "present"
                                        }
                                    },
                                    {
                                        "class": "ont",
                                        "name": "ONT-2",
                                        "description": "Optical Network Terminal",
                                        "uuid": "ont-uuid-002",
                                        "parent-component": "pon-xp2-uuid",
                                        "attributes": {
                                            "vendor": "CXNK",
                                            "serial": "478490",
                                            "product-code": "P8",
                                            "oper-state": "not-linked"
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        }

        # Restituiamo il JSON statico come dizionario
        return inventory_json, 200

# Registriamo il nuovo endpoint
def init_inventory_namespace(api):
    inventory_ns.add_resource(InventoryAPI, '/', endpoint="inventory")
    api.add_namespace(inventory_ns, path='/api/inventory')
