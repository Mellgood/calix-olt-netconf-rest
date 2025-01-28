from flask_restx import Namespace, Resource
from model.netconf.NetconfSession import NetconfSession
from model.api_model.ServiceModel import ServiceModel

ns = Namespace('service', description='Service management')
ns.add_model('ServiceModel', ServiceModel)

class ServiceAPI(Resource):
    @ns.expect(ServiceModel)
    def post(self):
        payload = ns.payload
        netconf_session = NetconfSession()

        try:
            response = netconf_session.create_service(
                ont_id=payload['ont_id'],
                cvlan=payload.get('cvlan'),
                ethernet_port=payload['ethernet_port'],
                svlan=payload['svlan'],
                profile=payload['profile'],
                bw=payload.get('bw')
            )
            if response is None:
                return {"error": "Failed to create service. No response from device."}, 500

            return {"message": "Service created successfully", "response": response.xml}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except RuntimeError as e:
            return {"error": str(e)}, 500



def init_service_namespace(api):
    ns.add_resource(ServiceAPI, '/', endpoint="create")
    api.add_namespace(ns, path='/api/service')
