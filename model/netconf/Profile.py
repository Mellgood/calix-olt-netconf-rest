class Profile:
    def __init__(self, element):
        self.element = element
        self.namespace = {'exa': 'http://www.calix.com/ns/exa/gpon-interface-base'}

    def get_name(self):
        name_element = self.element.find('exa:name', namespaces=self.namespace)
        return name_element.text if name_element is not None else None

    # Aggiungi qui altri metodi per accedere ad altre proprietà del profilo
