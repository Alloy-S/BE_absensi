from marshmallow import Schema, fields

class PaginationReq(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    search = fields.String(required=False, load_default="")