from flask_restx import fields, Model

ServiceModel = Model('ServiceModel', {
    'ont_id': fields.String(required=True, description="ID of the ONT to configure"),
    'cvlan': fields.String(required=False, description="Customer VLAN ID"),
    'ethernet_port': fields.String(required=True, description="Ethernet port of the ONT"),
    'svlan': fields.String(required=True, description="Service VLAN ID to configure"),
    'profile': fields.String(required=True, enum=["be", "ef"], description="QoS profile"),
    'bw': fields.String(required=False, description="Bandwidth, required if profile is 'ef'")
})
