from flask_restful import fields

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
        'harga_normal': fields.String,
        'harga_lembur': fields.String,
        'is_deleted': fields.Boolean,
    }))
}

harga_field = {
    "id": fields.String,
    "nama": fields.String,
    "harga_normal": fields.String,
    "is_deleted": fields.Boolean,
    "date": fields.String,
    "type": fields.String,
}

all_harga_field = {
    "items": fields.List(fields.Nested(harga_field)),
}

