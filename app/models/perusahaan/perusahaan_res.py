from flask_restful import fields

perusahaan_field = {
    "id": fields.String,
    "nama": fields.String,
    "alamat": fields.String,
    "kota_kabupaten": fields.String,
    "provinsi": fields.String,
    "negara": fields.String,
    "no_telepon": fields.String,
    "kode_pos": fields.String
}
