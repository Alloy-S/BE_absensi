from marshmallow import Schema, fields

class JabatanPaginationReq(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    search = fields.String(required=False)

class JabatanReq(Schema):
    nama = fields.String(required=True)
    parent_id = fields.String(required=False)