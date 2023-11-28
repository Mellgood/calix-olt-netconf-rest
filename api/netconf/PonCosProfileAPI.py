import os

from flask import jsonify, make_response
from flask_restx import Namespace, Resource, fields

from model.api_model.PonCosProfileModel import PonCosProfileModel
from model.netconf.NetconfSession import NetconfSession

ns = Namespace('PonCosProfile', description='Manage Running Configuration')
ns.add_model('PonCosProfileModel', PonCosProfileModel)

dev_env = os.getenv('DEV')

class PonCosProfileGetPutDelAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.running_config = kwargs.get('running_config')
        self.netconf_session = NetconfSession()

    def get(self, name=None):
        if self.running_config is None:
            return {'message': 'Internal server error'}, 500
        if name:
            profile = self.running_config.get_pon_cos_profile(name)
            if profile:
                return str(profile), 200
            else:
                return {'message': 'Profile not found'}, 404  # Not found
        else:
            # Logica per ottenere tutti i PonCosProfiles
            return {'message': 'List of all PonCosProfiles'}, 200

    def delete(self, name=None):
        # Logica per eliminare la configurazione
        return make_response({}, 501)  # Not implemented

    @ns.expect(PonCosProfileModel)
    def put(self, name=None):
        input_data = ns.payload
        if self.running_config is None:
            print(self.running_config)
            return {'message': 'Internal server error'}, 500
        if name:
            if name != input_data.get("name"):
                return {'message': 'Name missmatch.'}, 400  # Bad request
            # pc1.set_bandwidth(new_bw_type="explicit",new_max=4000000, new_min=4000000)
            profile = self.running_config.get_pon_cos_profile(name)
            if profile:
                # set_bandwidth(self, new_bw_type, new_max, new_min)
                profile.set_bandwidth(
                    new_bw_type=input_data.get("bandwidth_type"),
                    new_max=input_data.get("maximum_bw"),
                    new_min=input_data.get("min_bw")
                )

                if(dev_env):
                    print("[WARNING]: We are running in dev mode. No interaction with the OLT!")
                else:
                    self.netconf_session.netconf_edit_config(profile.generate_netconf_payload(), description=f"Apply values from REST API: {self.__class__.__name__}")
                return input_data, 200

            else:
                return {'message': 'Profile not found'}, 404  # Not found
        else:
            return {'message': 'A profile name must be passed.'}, 400
        # return make_response({}, 501) #Not implemented


class PonCosProfilePostAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.running_config = kwargs.get("running_config")
        self.netconf_session = NetconfSession()

    @ns.expect(PonCosProfileModel)
    def post(self):
        input_data = ns.payload
        if input_data is not None:
            for key, value in input_data.items():
                print(f"{key}: {value}")
            return {"message": input_data}, 501
        else:
            return {'message': 'No data received'}, 400  # Bad request


def init_pon_cos_profile_ns(api, running_config):
    ns.add_resource(PonCosProfileGetPutDelAPI, '/<string:name>',
                    resource_class_kwargs={'running_config': running_config})
    ns.add_resource(PonCosProfilePostAPI, '/', resource_class_kwargs={'running_config': running_config})
    api.add_namespace(ns, path='/api/pon-cos-profile')
