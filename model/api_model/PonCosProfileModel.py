from flask_restx import fields, Model

PonCosProfileModel = Model('PonCosProfileModel', {
    'name': fields.String(required=False, description="The name of the PonCosProfile."),
    'maximum_bw': fields.Integer(required=False, description='The maximum bandwidth'),
    "min_bw": fields.Integer(required=False, description="The minimum bandwidth."),
    "priority": fields.Integer(required=False, description="The priority to assign."),
    "bandwidth_type": fields.String(required=False, enum=["expedited", "assured"], description="The cos_type to assign.")
})
