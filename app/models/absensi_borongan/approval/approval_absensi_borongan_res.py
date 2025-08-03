from flask_restful import fields

harga_field = {
    'id': fields.String,
    'harga_normal': fields.Float,
    'harga_lembur': fields.Float,
    'nama': fields.String,
}

detail_fields = {
    'id': fields.String,
    'user_name': fields.String(attribute='user.fullname'),
    'ton_normal': fields.Float,
    'ton_lembur': fields.Float,
    'tipe': fields.String,
    'total': fields.Float,
    'harga': fields.Nested(harga_field),
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

user_field = {
    "id": fields.String,
    "fullname": fields.String,
    "jabatan": fields.String(attribute="data_karyawan.jabatan.nama"),
    "lokasi": fields.String(attribute="data_karyawan.lokasi.name"),
}

absensi_borongan_field = {
    'date': fields.String,
    'total': fields.Float,
    'detail_absensi_borongan': fields.List(fields.Nested(detail_fields)),
}

absensi_borongan_detail_fields = {
    'id': fields.String,
    'approval_user': fields.Nested(user_simple_field),
    'user': fields.Nested(user_field),
    'status': fields.String,
    'absensi_borongan': fields.Nested(absensi_borongan_field),
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
        'status': fields.String,
        'user': fields.Nested(user_simple_field),
        'total': fields.Float(attribute="absensi_borongan.total"),
    }))
}

history_borongan_pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'date': fields.String,
        'status': fields.String,
        'user': fields.Nested(user_simple_field, attribute="approval_absensi_borongan.user"),
        'total': fields.Float,
    }))
}

history_absensi_borongan_detail_fields = {
    'id': fields.String,
    'user': fields.Nested(user_field, attribute="approval_absensi_borongan.user"),
    'status': fields.String,
    'date': fields.String,
    'total': fields.Float,
    'detail_absensi_borongan': fields.List(fields.Nested(detail_fields)),
}
