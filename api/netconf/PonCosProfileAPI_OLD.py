from flask_restx import Namespace, Resource, fields

ns = Namespace('PonCosProfile', description='Operations related to PonCos Profiles')

# Modello per i dati di un PonCosProfile
profile_model = ns.model('PonCosProfile', {
    'name': fields.String(required=True, description='The name of the profile'),
    # Aggiungi qui altri campi necessari
})


#@ns.doc(params={'name': 'The name of the profile'})
class PonCosProfileAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.running_config = kwargs.get('running_config')

    def get(self, name=None):
        if self.running_config is None:
            print("Errore: running_config è None")
            return {'message': 'Internal server error'}, 500
        if name:
            # Logica per ottenere un singolo PonCosProfile per nome
            profile = self.running_config.get_pon_cos_profile(name)
            if profile:
                return profile, 200
            else:
                return {'message': 'Profile not found'}, 404
        else:
            # Logica per ottenere tutti i PonCosProfiles
            return {'message': 'List of all PonCosProfiles'}, 200

    @ns.expect(profile_model)
    def post(self):
        data = ns.payload
        # Logica per creare un nuovo PonCosProfile
        return {'message': 'Profile created', 'data': data}, 201

    @ns.expect(profile_model)
    def put(self, name):
        if name:
            data = ns.payload
            # Logica per aggiornare un PonCosProfile esistente
            return {'message': 'Profile updated', 'data': data}, 200
        else:
            return {'message': 'Profile name required for update'}, 400

    def delete(self, name):
        if name:
            # Logica per eliminare un PonCosProfile
            return {'message': 'Profile deleted'}, 204
        else:
            return {'message': 'Profile name required for deletion'}, 400


def init_pon_cos_profile_namespace(api, running_config):
    ns.add_resource(PonCosProfileAPI, '/', resource_class_kwargs={'running_config': running_config})
    api.add_namespace(ns, path='/api/pon-cos-profile/<string:name>')
