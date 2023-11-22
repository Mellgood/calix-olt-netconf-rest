from flask import jsonify, make_response
from flask_restx import Namespace, Resource, fields

ns = Namespace('RunningConfig', description='Manage Running Configuration')

model = ns.model('RunningConfigModel', {
    'data': fields.String(required=True, description='The configuration data')
})


class RunningConfigAPI(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.running_config = kwargs.get('running_config')

    def get(self):
        # Logica per ottenere la configurazione corrente
        #return {'status': '200', 'config': str(self.running_config.xml_data)}
        if self.running_config:
            xml_content = str(self.running_config.xml_data)
            return make_response(jsonify({'data': xml_content}), 200)


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


def init_running_config_namespace(api, running_config):
    ns.add_resource(RunningConfigAPI, '/', resource_class_kwargs={'running_config': running_config})
    api.add_namespace(ns, path='/api/running-config')
