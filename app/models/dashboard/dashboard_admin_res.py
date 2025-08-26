from flask_restful import fields

today_attendance_field = {
    'libur': fields.Boolean,
    'hadir': fields.Integer,
    'datang_terlambat': fields.Integer,
    'pulang_cepat': fields.Integer,
    'datang_terlambat_pulang_cepat': fields.Integer,
    'izin': fields.Integer,
    'alpha': fields.Integer,
}

total_users_field = {
    'user_bulanan': fields.Integer,
    'user_harian': fields.Integer,
}
