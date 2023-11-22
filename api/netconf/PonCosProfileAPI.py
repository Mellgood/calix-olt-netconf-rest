from flask import jsonify, make_response
from flask_restx import Namespace, Resource, fields

ns = Namespace('PonCosProfileAPI', description='Manage Running Configuration')

model = ns.model('PonCosProfileModel', {
    'data': fields.String(required=True, description='The configuration data')
})


class PonCosProfileAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.running_config = kwargs.get('running_config')

    def get(self, name=None):
        if self.running_config is None:
            return {'message': 'Internal server error'}, 500
        if name:
            profile = self.running_config.get_pon_cos_profile(name)
            if profile:
                return str(profile), 200
            else:
                return {'message': 'Profile not found'}, 404
        else:
            # Logica per ottenere tutti i PonCosProfiles
            return {'message': 'List of all PonCosProfiles'}, 200


    def post(self):
        input_data = ns.payload.get('data', None)
        if input_data is not None:
            print("Received data:", input_data)
            return {'message': 'Data received successfully'}, 200
        else:
            return {'message': 'No data received'}, 400

    def delete(self):
        # Logica per eliminare la configurazione
        return make_response({}, 418)


def init_pon_cos_profile_ns(api, running_config):
    ns.add_resource(PonCosProfileAPI, '/', resource_class_kwargs={'running_config': running_config})
    api.add_namespace(ns, path='/api/my-test/<string:name>')
