from model.xml.XMLHandler import XMLHandler


class Profile(XMLHandler):
    NAMESPACE = '{http://www.calix.com/ns/exa/gpon-interface-base}'


    def get_profile(self, name):
        for profile in self.find_elements('.//{}pon-cos-profile'.format(Profile.NAMESPACE)):
            if profile.find('{}name'.format(Profile.NAMESPACE)).text == name:
                return self._extract_profile_data(profile)
        return None

    def get_profiles(self):
        profiles = []
        for profile in self.find_elements('.//{}pon-cos-profile'.format(Profile.NAMESPACE)):
            profiles.append(self._extract_profile_data(profile))
        return profiles

    def _extract_profile_data(self, profile):
        return {
            'name': profile.find('{}name'.format(Profile.NAMESPACE)).text,
            'prio': profile.find('{}prio'.format(Profile.NAMESPACE)).text,
            'bw_type': profile.find('{}bw/{}type'.format(Profile.NAMESPACE, Profile.NAMESPACE)).text,
            'maximum': profile.find('{}bw/{}maximum'.format(Profile.NAMESPACE, Profile.NAMESPACE)).text,
            'minimum': profile.find('{}bw/{}minimum'.format(Profile.NAMESPACE, Profile.NAMESPACE)).text,
            'cos_type': profile.find('{}cos-type'.format(Profile.NAMESPACE)).text
        }

