from flask_restful import fields

detail_fields = {
    'id': fields.String,
    'ton_normal': fields.Float,
    'ton_lembur': fields.Float,
    'tipe': fields.String,
    'total': fields.Float,
    'harga_id': fields.String,
    'user_id': fields.String
}

approval_fields = {
    'status': fields.String,
    'approval_user_id': fields.String,
    'approval_user_name': fields.String
}

absensi_borongan_detail_fields = {
    'id': fields.String,
    'approval_user_id': fields.String,
    'approval_user_name': fields.String,
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
