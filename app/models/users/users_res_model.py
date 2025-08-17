from flask_restful import fields

user_fields = {
    'id': fields.String,
    'fullname': fields.String,
    'username': fields.String,
    'role': fields.String,
    'lokasi': fields.String,
    'jabatan': fields.String
}



posibe_user_pic = {
    'id': fields.String,
    'fullname': fields.String,
    'jabatan': fields.String
}

users_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'fullname': fields.String,
        'username': fields.String,
        'role': fields.String,
        'lokasi': fields.String,
        'jabatan': fields.String,
        'is_active': fields.Boolean,
    }))
}

users_cuti_kuota_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'fullname': fields.String,
        'sisa_cuti_tahunan': fields.Integer,
        'total_cuti_tahunan': fields.Integer
    }))
}

data_karyawan_fields = {
    'id': fields.String,
    'nip': fields.String,
    'tgl_gabung': fields.String,
    'tipe_karyawan': fields.String,
    'jabatan_id': fields.String(attribute='jabatan.id'),
    'jabatan': fields.String(attribute='jabatan.nama'),
    'jadwal_kerja_id': fields.String(attribute='jadwal_kerja.id'),
    'jadwal_kerja': fields.String(attribute='jadwal_kerja.shift'),
    'lokasi_id': fields.String(attribute='lokasi.id'),
    'lokasi': fields.String(attribute="lokasi.name"),
    'user_pic_id': fields.String,
    'user_pic_name': fields.String(attribute='pic.fullname'),
    'grup_gaji_id': fields.String,
    'gaji_pokok': fields.Float,
    'face_recognition_mode': fields.String(attribute='face_recognition_mode.value'),
}

data_pribadi_fields = {
    'id': fields.String,
    'gender': fields.String,
    'tgl_lahir': fields.String,
    'tmpt_lahir': fields.String,
    'status_kawin': fields.String,
    'agama': fields.String,
    'gol_darah': fields.String,
}

data_kontak_fields = {
    'id': fields.String,
    'alamat': fields.String,
    'no_telepon': fields.String,
    'nama_darurat': fields.String,
    'no_telepon_darurat': fields.String,
    'relasi_darurat': fields.String,
}

user_field = {
    'id': fields.String,
    'fullname': fields.String,
    'username': fields.String,
    'phone': fields.String,
    'role_id': fields.String(attribute='user_role.id'),
    'role': fields.String(attribute='user_role.name'),
    'data_karyawan': fields.Nested(data_karyawan_fields),
    'data_pribadi': fields.Nested(data_pribadi_fields),
    'data_kontak': fields.Nested(data_kontak_fields),
}

user_by_pic_field = {
    'items': fields.List(fields.Nested({
        'id': fields.String,
        'fullname': fields.String,
        'nip': fields.String,
        'jabatan': fields.String
    }))
}

simple_user_field = {
    "id": fields.String,
    "fullname": fields.String,
    "jabatan": fields.String(attribute="data_karyawan.jabatan.nama"),
    "lokasi": fields.String(attribute="data_karyawan.lokasi.name"),
}

all_approval_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'approval_id': fields.String,
        'tanggal_pengajuan': fields.String,
        'user': fields.String,
        'tipe_approval': fields.String,
        'status': fields.String,
    }))
}
