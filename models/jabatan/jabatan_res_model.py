from flask_restful import fields, reqparse

jabatan_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
        'parent_name': fields.String
    }))
}

jabatan_fields = {
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
    }))
}

jabatan_field = {
    'id': fields.String,
    'nama': fields.String,
    'parent_id': fields.String
}