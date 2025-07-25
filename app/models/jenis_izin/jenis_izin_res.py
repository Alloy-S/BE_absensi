from flask_restful import fields

jenis_izin_fields = {
    'id': fields.String,
    'nama': fields.String,
    'kuota_default': fields.Integer,
    'periode_reset': fields.String,
    'berlaku_setelah_bulan': fields.Integer
}

jenis_izin_pagination_fields = {
    "data": fields.List(fields.Nested(jenis_izin_fields), attribute='items'),
    "pagination": {
        "page": fields.Integer(attribute='page'),
        "per_page": fields.Integer(attribute='per_page'),
        "total_pages": fields.Integer(attribute='pages'),
        "total_items": fields.Integer(attribute='total')
    }
}

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested(jenis_izin_fields), attribute='items'),
}

jenis_izin_all_fields = {
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'nama': fields.String,
        'kuota_default': fields.Integer,
    }), attribute='items'),
}
