from flask_restx import Namespace, Resource

from model.api_model.TopologyData import topology_data

topology_ns = Namespace('topology', description='Static Topology JSON')

#mock data
TOPOLOGY_DATA = topology_data


class TopologyAPI(Resource):
    def get(self):
        return TOPOLOGY_DATA, 200


def init_topology_namespace(api):
    topology_ns.add_resource(TopologyAPI, '/', endpoint="topology")
    api.add_namespace(topology_ns, path='/api/topology')
