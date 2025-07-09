from flask_restful import fields

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
        'harga_normal': fields.String,
        'harga_lembur': fields.String,
    }))
}

harga_field = {
    "id": fields.String,
    "nama": fields.String,
    "harga_normal": fields.Float,
    "harga_lembur": fields.Float,
    "jam_start_normal": fields.String,
    "jam_end_normal": fields.String,
    "toleransi_waktu": fields.String,
    "grup_id": fields.String,
    "is_deleted": fields.Boolean,
    "date": fields.String,
    "type": fields.String
}

all_harga_field = {
    "items": fields.List(fields.Nested(harga_field)),
}

