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

        print(payload)

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
                return {"message": "Service created successfully", "Service": payload}, 200

            return {"message": "Service created successfully", "response": response}, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except RuntimeError as e:
            return {"error": str(e)}, 500

    @ns.expect(ServiceModel)
    def delete(self):
        payload = ns.payload
        netconf_session = NetconfSession()

        print(payload)

        try:
            response = netconf_session.delete_service(
                ont_id=payload['ont_id'],
                ethernet_port=payload['ethernet_port'],
                svlan=payload['svlan'],
                profile=payload['profile']
            )
            return {"message": "Service deleted successfully", "response": response}, 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except RuntimeError as e:
            return {"error": str(e)}, 500


def init_service_namespace(api):
    ns.add_resource(ServiceAPI, '/', endpoint="create")
    api.add_namespace(ns, path='/api/service')
