from flask_restx import Namespace, Resource

ns = Namespace('config', description='Configuration operations')


@ns.route('/', tags=["asd"])
class RunningConfig(Resource):
    def get(self):
        # Implementa la logica per ottenere la configurazione corrente
        return {'status': 'running', 'config': 'your_config_here'}
