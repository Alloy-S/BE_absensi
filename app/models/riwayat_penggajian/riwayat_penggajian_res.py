from flask_restful import fields

riwayat_penggajian_rincian_field = {
    'komponen': fields.String,
    'tipe': fields.String,
    'jumlah': fields.String,
    'nilai_a': fields.String,
    'nilai_b': fields.String,
    'operasi': fields.String,
}

riwayat_penggajian_detail_field = {
    'total_tunjangan': fields.String,
    'total_potongan': fields.String,
    'gaji': fields.String,
    'user_id': fields.String,
    'user': fields.String(attribute="user.fullname"),
    'riwayat_penggajian_rincian': fields.List(fields.Nested(riwayat_penggajian_rincian_field)),
}

riwayat_penggajian_field = {
    'id': fields.String,
    'periode_start': fields.String,
    'periode_end': fields.String,
    'status': fields.String,
    'total_karyawan': fields.Integer,
    'total_gaji_keseluruhan': fields.String,
    'created_by': fields.String(attribute="user.fullname"),
    'grup_gaji': fields.String(attribute="grup_gaji.grup_name"),
    'riwayat_penggajian_detail': fields.List(fields.Nested(riwayat_penggajian_detail_field)),
}

riwayat_penggajian_pagination_item = {
    'id': fields.String,
    'periode_start': fields.String,
    'periode_end': fields.String,
    'status': fields.String,
    'grup_name': fields.String,
}


riwayat_penggajian_pagination = {
    "pages": fields.Integer,
    "total": fields.Integer,
    'items': fields.List(fields.Nested(riwayat_penggajian_pagination_item))
}

export_excel_field = {
    'filename': fields.String,
    'file': fields.String,
}
