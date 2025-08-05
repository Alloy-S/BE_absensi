from flask_restful import fields




jadwal_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'kode': fields.String,
        'shift': fields.String,
        'is_active': fields.Boolean,
    }))
}

jadwal_fields = {
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'kode': fields.String,
        'shift': fields.String
    }))
}

jadwal_kerja_detail_fields = {
    'id': fields.String,
    'hari': fields.String(attribute='hari_str'),
    'time_in': fields.String(attribute='jam_in_str'),
    'time_out': fields.String(attribute='jam_out_str'),
    'toler_in': fields.Integer,
    'toler_out': fields.Integer,
    'is_active': fields.Boolean
}


jadwal_kerja_field = {
    'id': fields.String,
    'kode': fields.String,
    'shift': fields.String,
    'is_active': fields.Boolean,
    'detail_jadwal_kerja': fields.List(fields.Nested(jadwal_kerja_detail_fields))
}


