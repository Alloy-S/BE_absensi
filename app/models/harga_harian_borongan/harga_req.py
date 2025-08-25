from marshmallow import Schema, fields

class HargaReq(Schema):
    nama = fields.Str(required=True)
    harga_normal = fields.Float(required=True)
    type = fields.Str(required=True)