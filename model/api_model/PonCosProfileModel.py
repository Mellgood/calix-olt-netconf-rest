from flask_restx import fields, Model

PonCosProfileModel = Model('PonCosProfileModel', {
    'name': fields.String(required=False, description="The name of the PonCosProfile."),
    "priority": fields.Integer(required=False, description="The priority to assign."),
    "bandwidth_type": fields.String(required=False, enum=["explicit"], description="The cos_type to assign."), #TBD enum types
    'maximum_bw': fields.Integer(required=False, description='The maximum bandwidth'),
    "min_bw": fields.Integer(required=False, description="The minimum bandwidth."),
    "cos_type": fields.Integer(required=False, enum=["expedited", "assured"], description="The minimum bandwidth."),
})
#"PonCosProfile(Name: ont1_assured, Priority: 2, Bandwidth: Type: explicit, Maximum: 1000000, Minimum: 1000000, COS Type: assured)"