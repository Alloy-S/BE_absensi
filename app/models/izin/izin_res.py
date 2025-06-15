from flask_restful import fields

approval_izin_field = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user_id': fields.String,
    'izin_id': fields.String,
    'user_id': fields.String
}

approval_izin_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'created_date': fields.String,
        'status': fields.String,
        'approval_user_id': fields.String,
        'izin_id': fields.String,
        'user_id': fields.String,
    }))
}

izin_field = {
    'id': fields.String,
    'date': fields.String,
    'tgl_izin_start': fields.String,
    'tgl_izin_end': fields.String,
    'keterangan': fields.String,
    'status': fields.String,
    'jenis_izin_id': fields.String,
    'user_id': fields.String
}

approval_izin_field_detail = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user_id': fields.String,
    'user_id': fields.String,
    'izin': fields.Nested(izin_field)
}
