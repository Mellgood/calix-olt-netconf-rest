from ncclient import manager
from termcolor import colored


class NetconfSession:
    def __init__(self, host, port, username, password):
        self.session = manager.connect_ssh(host=host, port=port, username=username, password=password,
                                           hostkey_verify=False)

    def _check_response(self, rpc_obj, snippet_name):
        # print("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
        xml_str = rpc_obj.xml
        if "<ok/>" in xml_str:
            print("%s: SUCCESSFUL" % snippet_name)
        else:
            print("ERROR: Cannot successfully execute: %s" % snippet_name)

    def netconf_edit_config(self, xml_config, description="NO DESCRIPTION FOR THIS edit_config command PROVIDED"):
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
        try:
            netconf_response = self.session.get_config(source=source)
            return netconf_response
        except Exception as e:
            message = "[ERROR]: " + str(e.__class__) + " occurred."
            print(colored(message, "red"))
            print(colored(str(e), "red"))
            return None


