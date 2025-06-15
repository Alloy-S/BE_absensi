from flask_restful import fields

approval_lembur_field = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user_id': fields.String,
    'lembur_id': fields.String,
    'user_id': fields.String
}

approval_lembur_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'created_date': fields.String,
        'status': fields.String,
        'approval_user_id': fields.String,
        'lembur_id': fields.String,
        'user_id': fields.String,
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

approval_lembur_field_detail = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user_id': fields.String,
    'user_id': fields.String,
    'lembur': fields.Nested(lembur_field)
}
