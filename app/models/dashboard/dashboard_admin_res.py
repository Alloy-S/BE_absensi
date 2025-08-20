from flask_restful import fields

today_attendance_field = {
    'hadir': fields.Integer,
    'terlambat': fields.Integer,
    'pulang_cepat': fields.Integer,
    'terlambat_pulang_cepat': fields.Integer,
    'izin': fields.Integer,
    'alpha': fields.Integer,
}

total_users_field = {
    'total_active_users': fields.Integer,
}
