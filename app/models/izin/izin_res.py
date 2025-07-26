from flask_restful import fields

from app.entity import jenis_izin

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

jenis_izin_field = {
    'id': fields.String,
    'nama': fields.String
}

izin_field = {
    'id': fields.String,
    'date': fields.String,
    'tgl_izin_start': fields.String,
    'tgl_izin_end': fields.String,
    'keterangan': fields.String,
    'status': fields.String,
    'jenis_izin': fields.Nested(jenis_izin_field),
    'user_id': fields.String
}

user_simple_field = {
    "id": fields.String,
    "fullname": fields.String
}

approval_izin_field_detail = {
    'id': fields.String,
    'created_date': fields.String,
    'status': fields.String,
    'approval_user': fields.Nested(user_simple_field),
    'user_id': fields.String,
    'izin': fields.Nested(izin_field)
}


