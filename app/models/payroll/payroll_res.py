from flask_restful import fields

rincian_perhitung_field = {
    'komponen': fields.String,
    'tipe': fields.String,
    'jumlah': fields.Float,
    'nilai_a': fields.String,
    'nilai_b': fields.String,
    'operasi': fields.String,
}

hasil_penggajian_field = {
    'user_id': fields.String,
    'nama_karyawan': fields.String,
    'total_tunjangan': fields.Float,
    'total_potongan': fields.Float,
    'gaji': fields.Float,
    'rincian': fields.List(fields.Nested(rincian_perhitung_field)),
}

proses_penggajian_field = {
    'riwayat_id': fields.String,
    'data': fields.Nested(hasil_penggajian_field),
}
