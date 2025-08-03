from flask_restful import fields

from app.models.users.users_res_model import simple_user_field

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

absensi_pagination_admin_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'date': fields.String,
        'lokasi': fields.String,
        'metode': fields.String,
        'status': fields.String,
        'user': fields.Nested(simple_user_field),
    }))
}

absensi_detail_fields = {
    'id': fields.String,
    'date': fields.String,
    'lokasi': fields.String,
    'metode': fields.String,
    'status': fields.String,
    'user_id': fields.String,
    'user': fields.Nested(simple_user_field),
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

check_today_attendance = {
    "status": fields.String,
    "required_attendance_type": fields.String,
    "time_clock_in": fields.String,
    "time_clock_out": fields.String,
    "today": fields.String,
    "shift": fields.String,
}

check_attendance_by_date = {
    "date": fields.String,
    "absensi_id": fields.String,
    "time_in": fields.String,
    "time_out": fields.String,
}
