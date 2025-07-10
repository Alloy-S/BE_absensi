from marshmallow import Schema, fields

class PengumumanReq(Schema):
    judul = fields.Str(required=True)
    isi = fields.Str(required=True)
    is_active = fields.Boolean(required=True)