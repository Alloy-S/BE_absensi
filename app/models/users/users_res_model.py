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
        'jabatan': fields.String
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
