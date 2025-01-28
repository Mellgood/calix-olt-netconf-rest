import json
import xml.etree.ElementTree as ET
from model.api_model.ServiceModel import ServiceModel


class PonCosProfile:
    def __init__(self, element):
        self.element = element
        self.namespace = {'exa': 'http://www.calix.com/ns/exa/gpon-interface-base'}

        self.name = self._get_text('exa:name')
        self.priority = self._get_text('exa:prio')
        self.cos_type = self._get_text('exa:cos-type')
        bw_element = self.element.find('exa:bw', namespaces=self.namespace)
        self.bandwidth_type = self._get_text('exa:type', bw_element)
        self.bandwidth_max = self._get_text('exa:maximum', bw_element)
        self.bandwidth_min = self._get_text('exa:minimum', bw_element)


    def __str__(self):
        bandwidth = self.get_bandwidth()
        bw_str = f"Type: {bandwidth['type']}, Maximum: {bandwidth['maximum']}, Minimum: {bandwidth['minimum']}" if bandwidth else "Not set"
        return (f"PonCosProfile(Name: {self.get_name()}, "
                f"Priority: {self.get_priority()}, "
                f"Bandwidth: {bw_str}, "
                f"COS Type: {self.get_cos_type()})")

    def get_name(self):
        return self._get_text('exa:name')

    def get_priority(self):
        return self._get_text('exa:prio')

    def get_bandwidth(self):
        bw_element = self.element.find('exa:bw', namespaces=self.namespace)
        if bw_element is not None:
            return {
                'type': self._get_text('exa:type', bw_element),
                'maximum': self._get_text('exa:maximum', bw_element),
                'minimum': self._get_text('exa:minimum', bw_element)
            }
        return None

    def get_cos_type(self):
        return self._get_text('exa:cos-type')

    def _get_text(self, tag, element=None):
        if element is None:
            element = self.element
        found_element = element.find(tag, namespaces=self.namespace)
        return found_element.text if found_element is not None else None

        # Setter per il nome
    def set_name(self, new_name):
        name_element = self.element.find('exa:name', namespaces=self.namespace)
        if name_element is not None:
            name_element.text = new_name

    # Setter per la priorità
    def set_priority(self, new_priority):
        prio_element = self.element.find('exa:prio', namespaces=self.namespace)
        if prio_element is not None:
            prio_element.text = str(new_priority)

    # Setter per il tipo COS
    def set_cos_type(self, new_cos_type):
        cos_type_element = self.element.find('exa:cos-type', namespaces=self.namespace)
        if cos_type_element is not None:
            cos_type_element.text = new_cos_type

    # Setter per la banda larga
    def set_bandwidth(self, new_bw_type, new_max, new_min):
        bw_element = self.element.find('exa:bw', namespaces=self.namespace)
        if bw_element is not None:
            self._set_text('exa:type', new_bw_type, bw_element)
            self._set_text('exa:maximum', str(new_max), bw_element)
            self._set_text('exa:minimum', str(new_min), bw_element)

    def _set_text(self, tag, new_text, parent_element):
        element = parent_element.find(tag, namespaces=self.namespace)
        if element is not None:
            element.text = new_text

    def generate_netconf_payload(self):
        """
        Genera un payload NETCONF per la configurazione del pon-cos-profile.
        :return: Stringa XML per il payload NETCONF.
        """
        config_element = ET.Element("config")
        base_config = ET.SubElement(config_element, "config", xmlns="http://www.calix.com/ns/exa/base")
        profile_element = ET.SubElement(base_config, "profile")
        pon_cos_profile_element = ET.SubElement(profile_element, "pon-cos-profile",
                                                xmlns="http://www.calix.com/ns/exa/gpon-interface-base")

        # Aggiungi elementi figli basati sugli attributi dell'oggetto
        ET.SubElement(pon_cos_profile_element, "name").text = self.get_name()
        ET.SubElement(pon_cos_profile_element, "prio").text = self.get_priority()
        bw_element = ET.SubElement(pon_cos_profile_element, "bw")
        ET.SubElement(bw_element, "type").text = self.get_bandwidth()["type"]
        ET.SubElement(bw_element, "maximum").text = self.get_bandwidth()["maximum"]
        ET.SubElement(bw_element, "minimum").text = self.get_bandwidth()["minimum"]
        ET.SubElement(pon_cos_profile_element, "cos-type").text = self.get_cos_type()

        # Costruzione del payload NETCONF
        netconf_payload = ET.tostring(config_element, encoding="unicode")
        return netconf_payload

    def get_data(self):
        profile_data = {
            "name": self.name,
            "priority": self.get_priority(),
            "bandwidth_type": self.bandwidth_type,
            "maximum_bw": self.bandwidth_max,
            "min_bw": self.bandwidth_min,
            "cos_type": self.cos_type
        }
        return profile_data

