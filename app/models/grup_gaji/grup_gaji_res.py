from flask_restful import fields

komponen_grup_gaji_fields = {
    'kom_id': fields.String,
    'use_kondisi': fields.Boolean,
    'kode_kondisi': fields.String,
    'min_kondisi': fields.Integer,
    'max_kondisi': fields.Integer,
    'use_formula': fields.Boolean,
    'kode_formula': fields.String,
    'operation_sum': fields.String,
    'nilai_statis': fields.String,
    'use_nilai_dinamis': fields.Boolean,
    'kode_nilai_dinamis': fields.String,
}

grup_gaji_fields = {
    'id': fields.String,
    'grup_kode': fields.String,
    'grup_name': fields.String,
    'komponen': fields.List(fields.Nested(komponen_grup_gaji_fields), attribute='grup_gaji_kom')
}

grup_gaji_pagination_fields = {
    'total': fields.Integer,
    'pages': fields.Integer,
    'items': fields.List(fields.Nested({
        'id': fields.String,
        'grup_kode': fields.String,
        'grup_name': fields.String,
    })),
}

kode_perhitungan_fields = {
    'kode': fields.String,
    'name': fields.String,
}

simple_grup_gaji_fields = {
    'id': fields.String,
    'grup_kode': fields.String,
    'grup_name': fields.String,
}

grup_gaji_users_fields = {
    'grup_gaji': fields.Nested(simple_grup_gaji_fields),
    'list_karyawan': fields.List(fields.Nested({
        'nip': fields.String,
        'fullname': fields.String,
        'jabatan': fields.String,
    })),
}
