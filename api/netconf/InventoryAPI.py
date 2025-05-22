from flask_restx import Namespace, Resource
import xml.etree.ElementTree as ET

from model.netconf.NetconfSession import NetconfSession

inventory_ns = Namespace('inventory', description='Network Hardware Inventory')


def safe_find_text(element, tag, ns):
    found = element.find(tag, ns)
    return found.text if found is not None else None


class InventoryAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.netconf_session = NetconfSession()

    def get(self):
        inventory_request = """
        <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
              <pon xmlns="http://www.calix.com/ns/exa/gpon-interface-std">
                <discovered-onts/>
              </pon>
              <name/>
            </interface>
        </interfaces-state>
        """

        try:
            response = self.netconf_session.session.get(filter=("subtree", inventory_request))
            xml_data = response.xml

            root = ET.fromstring(xml_data)
            ns = {
                'nc': 'urn:ietf:params:xml:ns:netconf:base:1.0',
                'if': 'urn:ietf:params:xml:ns:yang:ietf-interfaces',
                'gpon': 'http://www.calix.com/ns/exa/gpon-interface-std'
            }

            # Base JSON
            inventory_json = {
                "ietf-network-hardware-inventory:network-hardware-inventory": {
                    "network-elements": {
                        "network-element": [
                            {
                                "name": "OLT",
                                "uuid": "olt-uuid-001",
                                "components": {
                                    "component": []
                                }
                            }
                        ]
                    }
                }
            }

            olt_components = inventory_json["ietf-network-hardware-inventory:network-hardware-inventory"]["network-elements"]["network-element"][0]["components"]["component"]

            # Add OLT component
            olt_component = {
                "class": "olt",
                "name": "OLT",
                "description": "Optical Line Terminal",
                "uuid": "olt-uuid-001",
                "attributes": {
                    "port": "xp1"
                },
                "child-components": []
            }
            olt_components.append(olt_component)

            ont_counter = 1

            for iface in root.findall('.//if:interface', ns):
                name_elem = iface.find('if:name', ns)
                if name_elem is not None:
                    port_name = name_elem.text

                    if port_name and "xp" in port_name:
                        port_uuid = f"pon-{port_name}-uuid"
                        port_component = {
                            "class": "port",
                            "name": port_name,
                            "description": "Passive Optical Network port",
                            "uuid": port_uuid,
                            "parent-component": "olt-uuid-001",
                            "attributes": {
                                "admin-state": "up",
                                "oper-state": "up"
                            },
                            "child-components": []
                        }

                        # Link port as child of OLT
                        olt_component["child-components"].append(port_uuid)

                        # Add the port component to the main list
                        olt_components.append(port_component)

                        discovered_onts = iface.findall('.//gpon:discovered-ont', ns)
                        for ont in discovered_onts:
                            serial = safe_find_text(ont, 'gpon:serial-number', ns) or "<unknown>"
                            vendor = safe_find_text(ont, 'gpon:vendor-id', ns) or "<unknown>"
                            product_code = safe_find_text(ont, 'gpon:product-code', ns) or "<unknown>"
                            ont_id = safe_find_text(ont, 'gpon:ont-id', ns) or f"{ont_counter}"

                            ont_uuid = f"ont-uuid-{ont_counter:03d}"
                            ont_component = {
                                "class": "ont",
                                "name": f"ONT-{ont_counter}",
                                "description": "Optical Network Terminal",
                                "uuid": ont_uuid,
                                "parent-component": port_uuid,
                                "attributes": {
                                    "vendor": vendor,
                                    "serial": serial,
                                    "product-code": product_code,
                                    "oper-state": "present"
                                }
                            }

                            # Add the ONT component to the main list
                            olt_components.append(ont_component)

                            # Link ONT as child of its port
                            port_component["child-components"].append(ont_uuid)

                            ont_counter += 1

            return inventory_json, 200

        except Exception as e:
            return {"error": f"Failed to get inventory: {str(e)}"}, 500


def init_inventory_namespace(api):
    inventory_ns.add_resource(InventoryAPI, '/', endpoint="inventory")
    api.add_namespace(inventory_ns, path='/api/inventory')
