from flask_restful import fields

approval_lembur_field = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user_id': fields.String,
    'lembur_id': fields.String,
    'user_id': fields.String
}

user_field = {
    "id": fields.String,
    "fullname": fields.String,
    "jabatan": fields.String(attribute="data_karyawan.jabatan.nama"),
    "lokasi": fields.String(attribute="data_karyawan.lokasi.name"),
}

approval_lembur_pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'created_date': fields.String,
        'status': fields.String,
        'date_start': fields.String(attribute="lembur.date_start"),
        'date_end': fields.String(attribute="lembur.date_end"),
        # 'user': fields.Nested(user_field),
        'approval_user': fields.String(attribute="approval_user.fullname"),
    }))
}

history_lembur_pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'status': fields.String,
        'date_start': fields.String,
        'date_end': fields.String,
        'user': fields.Nested(user_field),
    }))
}

lembur_field = {
    'id': fields.String,
    'date_start': fields.String,
    'date_end': fields.String,
    'keterangan': fields.String,
    'status': fields.String,
    'user_id': fields.String
}

history_lembur_field = {
    'id': fields.String,
    'date_start': fields.String,
    'date_end': fields.String,
    'keterangan': fields.String,
    'status': fields.String,
    'user': fields.Nested(user_field),
}

user_simple_field = {
    "id": fields.String,
    "fullname": fields.String
}

approval_lembur_field_detail = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user': fields.Nested(user_simple_field),
    'user': fields.Nested(user_field),
    'lembur': fields.Nested(lembur_field)
}
