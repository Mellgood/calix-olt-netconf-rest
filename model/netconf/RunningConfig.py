import xml.etree.ElementTree as ET

from model.netconf.PonCosProfile import PonCosProfile
from model.netconf.Profile import Profile


class RunningConfig:
    def __init__(self, xml_data):
        self.xml_data = xml_data
        self.tree = ET.ElementTree(ET.fromstring(str(xml_data)))
        self.namespace = {'exa': 'http://www.calix.com/ns/exa/gpon-interface-base'}

    def get_profile(self, profile_name):
        xpath = f".//exa:ont-profile[exa:name='{profile_name}']"
        profile_element = self.tree.find(xpath, namespaces=self.namespace)
        return Profile(profile_element) if profile_element is not None else None

    def get_all_profile_names(self):
        profile_names = []
        for profile in self.tree.findall('.//exa:ont-profile/exa:name', namespaces=self.namespace):
            profile_names.append(profile.text)
        return profile_names

    def get_pon_cos_profile(self, profile_name):
        xpath = f".//exa:pon-cos-profile[exa:name='{profile_name}']"
        profile_element = self.tree.find(xpath, namespaces=self.namespace)
        return PonCosProfile(profile_element) if profile_element is not None else None

    def get_pon_cos_profiles(self):
        profiles = []
        for profile_elem in self.tree.findall('.//exa:pon-cos-profile', namespaces=self.namespace):
            profiles.append(PonCosProfile(profile_elem))
        return profiles


    # Aggiungi qui altri metodi utili per gestire l'intera configurazione
