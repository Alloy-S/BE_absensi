from flask_restful import fields

from app.models.harga_harian_borongan.harga_res import harga_field

detail_fields = {
    'id': fields.String,
    'ton_normal': fields.Float,
    'ton_lembur': fields.Float,
    'tipe': fields.String,
    'total': fields.Float,
    'harga': fields.Nested(harga_field),
    'user_name': fields.String(attribute='user.fullname'),
}

harga_field = {
    'id': fields.String,
    'ton_normal': fields.Float,
    'ton_lembur': fields.Float,
    'nama': fields.String,
}

approval_fields = {
    'status': fields.String,
    'approval_user_id': fields.String,
    'approval_user_name': fields.String
}

user_simple_field = {
    "id": fields.String,
    "fullname": fields.String
}

absensi_borongan_detail_fields = {
    'id': fields.String,
    'approval_user': fields.Nested(user_simple_field),
    'status': fields.String,
    'date': fields.String,
    'total': fields.Float,
    'details': fields.List(fields.Nested(detail_fields)),
}

approval_absensi_borongan_detail_fields = {
    'id': fields.String,
    'created_date': fields.String,
}

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'created_date': fields.String,
        'status': fields.String
    }))
}
