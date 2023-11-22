import xml.etree.ElementTree as ET

class XMLHandler:
    def __init__(self, xml_data):
        self.root = ET.fromstring(xml_data)

    def find_element(self, path):
        return self.root.find(path)

    def find_elements(self, path):
        return self.root.findall(path)