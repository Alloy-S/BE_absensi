from marshmallow import Schema, fields

class JabatanReq(Schema):
    nama = fields.String(required=True)
    parent_id = fields.String(required=False, allow_none=True)