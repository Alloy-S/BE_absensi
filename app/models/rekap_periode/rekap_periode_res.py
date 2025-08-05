from flask_restful import fields

rekap_periode_field = {
    'nip': fields.String,
    'nama': fields.String,
    'tipe_karyawan': fields.String,
    'jabatan': fields.String,
    'lokasi': fields.String,
    'total_kehadiran': fields.String,
    'total_izin': fields.String,
    'total_tidak_hadir': fields.String,
    'total_absen_tidak_lengkap': fields.String,
    'total_terlambat': fields.String,
    'total_pulang_awal': fields.String,
    'total_menit_kehadiran': fields.String,
    'total_menit_terlambat': fields.String,
    'total_menit_pulang_awal': fields.String,
}

rekap_pagination = {
    "pages": fields.String,
    "total": fields.String,
    'items': fields.List(fields.Nested(rekap_periode_field))
}
