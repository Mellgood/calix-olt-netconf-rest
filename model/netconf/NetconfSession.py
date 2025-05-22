import os

from ncclient import manager
from termcolor import colored

from model.netconf.seasonnetconfdemo.PON import create_service, delete_service

dev_run = os.getenv('DEV')
dev_run = False


class NetconfSession:
    _instance = None
    _is_initialized = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(NetconfSession, cls).__new__(cls)
        return cls._instance

    def __init__(self, host=None, port=None, username=None, password=None):
        if not self._is_initialized:
            self.host = host
            self.port = port
            self.username = username
            self.password = password
            if dev_run:
                print("[WARNING]: We are running in dev mode. No interaction with the OLT!")
            else:
                self.session = manager.connect_ssh(host=self.host, port=self.port, username=self.username,
                                                   password=self.password,
                                                   hostkey_verify=False)
            self._is_initialized = True
        else:
            # Controlla se i parametri sono diversi e avvisa
            if (self.host != host or self.port != port or
                    self.username != username or self.password != password):
                print(f"[WARNING]: Someone is trying to initialize {self.__class__.__name__} with different "
                      f"parameters. This will result in no effect.")

    def _check_response(self, rpc_obj, snippet_name):
        xml_str = rpc_obj.xml if rpc_obj else "<No Response>"
        if "<ok/>" in xml_str:
            print(f"{snippet_name}: SUCCESSFUL")
        else:
            print(f"ERROR: {snippet_name} failed with response: {xml_str}")

    def netconf_edit_config(self, xml_config, description="NO DESCRIPTION FOR THIS edit_config command PROVIDED"):
        if dev_run:
            print("[WARNING]: We are running in dev mode. No interaction with the OLT!")
            return "Mock response from the OLT"
        try:
            netconf_response = self.session.edit_config(target="running", config=xml_config)
            self._check_response(netconf_response, description)
            return netconf_response
        except Exception as e:
            message = "[ERROR]: " + str(e.__class__) + " occurred."
            print(colored(message, 'red'))
            print(colored(str(e), 'red'))
            return None

    def netconf_get(self, filter_xml=None, description="NO DESCRIPTION FOR THIS get command PROVIDED"):
        if dev_run:
            print("[WARNING]: We are running in dev mode. No interaction with the OLT!")
            return "Mock response from the OLT"
        try:
            netconf_response = self.session.get(filter=filter_xml)
            self._check_response(netconf_response, description)
            return netconf_response
        except Exception as e:
            message = "[ERROR]: " + str(e.__class__) + " occurred."
            print(colored(message, "red"))
            print(colored(str(e), "red"))
            return None

    def netconf_get_config(self, source="running", description="NO DESCRIPTION FOR THIS get_config command PROVIDED"):
        if dev_run:
            print("[WARNING]: We are running in dev mode. No interaction with the OLT!")
            return "Mock response from the OLT"
        try:
            netconf_response = self.session.get_config(source=source)
            return netconf_response
        except Exception as e:
            message = "[ERROR]: " + str(e.__class__) + " occurred."
            print(colored(message, "red"))
            print(colored(str(e), "red"))
            return None

    def create_service(self, ont_id, cvlan, ethernet_port, svlan, profile, bw=None):
        """
        Creates and configures a service on an ONT.
        """
        try:
            return create_service(self.session, ont_id, cvlan, ethernet_port, svlan, profile, bw=bw)
        except Exception as e:
            raise RuntimeError(f"NETCONF create_service failed: {str(e)}")

    def delete_service(self, ont_id, ethernet_port, svlan, profile):
        """
        Deletes a configured service from an ONT.
        """
        try:
            return delete_service(self.session, ont_id, ethernet_port, svlan, profile)
        except Exception as e:
            raise RuntimeError(f"NETCONF delete_service failed: {str(e)}")

    def get_inventory(self):
        # XML per ottenere l'inventario hardware della rete
        inventory_request = """
        <rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
          <get>
            <filter type="subtree">
              <ietf-network-hardware-inventory:network-hardware-inventory xmlns:ietf-network-hardware-inventory="urn:ietf:params:xml:ns:yang:ietf-network-hardware-inventory">
              </ietf-network-hardware-inventory:network-hardware-inventory>
            </filter>
          </get>
        </rpc>
        """

        try:
            response = self.session.dispatch(inventory_request)
            return response
        except Exception as e:
            print(f"Error getting inventory: {e}")
            return None
