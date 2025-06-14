from flask_restful import fields

absensi_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'date': fields.String,
        'lokasi': fields.String,
        'metode': fields.String,
        'status': fields.String,
        'user_id': fields.String,
    }))
}

absensi_detail_fields = {
    'id': fields.String,
    'date': fields.String,
    'lokasi': fields.String,
    'metode': fields.String,
    'status': fields.String,
    'user_id': fields.String,
    "detail_absensi": fields.List(fields.Nested({
        'id': fields.String,
        'date': fields.String,
        'type': fields.String,
        'status_appv': fields.String,
        'status_absensi': fields.String,
        'latitude': fields.String,
        'longitude': fields.String,
        'catatan': fields.String,
    }))
}
