from flask_restful import fields

jenis_izin_simple_fields = {
    'id': fields.String,
    'nama': fields.String
}


jatah_cuti_fields = {
    'id': fields.String,
    'periode': fields.Integer,
    'kuota_awal': fields.Integer,
    'kuota_terpakai': fields.Integer,
    'sisa_kuota': fields.Integer,
    'user_id': fields.String,
    'jenis_izin': fields.Nested(jenis_izin_simple_fields)
}

user_field = {
    'id': fields.String,
    'fullname': fields.String,
    'nip': fields.String(attribute='data_karyawan.nip'),
    'jabatan': fields.String(attribute='data_karyawan.jabatan.nama'),
    'lokasi': fields.String(attribute='data_karyawan.lokasi.name'),
}

pagination_fields = {
    'user': fields.Nested(user_field),
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested(jatah_cuti_fields), attribute='items'),
}