from marshmallow import Schema, fields

class LokasiReq(Schema):
    name = fields.Str(required=True)
    longitude = fields.Float(required=True)
    latitude = fields.Float(required=True)
    toleransi = fields.Int(required=True)