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

datang_terlambat_field = {
    'nip': fields.String,
    'nama': fields.String,
    'jabatan': fields.String,
    'lokasi': fields.String,
    'jadwal_kerja': fields.String,
    'date_absensi': fields.String,
    'waktu_absen': fields.String,
    'jadwal_time_in': fields.String,
    'menit_terlambat': fields.Float,
}

kuota_cuti_field = {
    'nip': fields.String,
    'nama': fields.String,
    'periode': fields.String,
    'sisa_cuti_tahunan': fields.Integer,
    'total_cuti_tahunan': fields.Integer,
    'cuti_tahunan_terpakai': fields.Integer,
}

rekap_pagination = {
    "pages": fields.Integer,
    "total": fields.Integer,
    'items': fields.List(fields.Nested(rekap_periode_field))
}

datang_terlambat_pagination = {
    "pages": fields.Integer,
    "total": fields.Integer,
    'items': fields.List(fields.Nested(datang_terlambat_field))
}

kuota_cuti_pagination = {
    "pages": fields.Integer,
    "total": fields.Integer,
    'items': fields.List(fields.Nested(kuota_cuti_field))
}