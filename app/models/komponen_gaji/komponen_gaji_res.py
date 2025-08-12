from flask_restful import fields

kom_gaji_fields = {
    'id': fields.String,
    'kom_kode': fields.String,
    'kom_name': fields.String,
    'no_urut': fields.String,
    'tipe': fields.String(attribute="tipe.value"),
    'hitung': fields.String(attribute="hitung.value"),
}

kom_gaji_pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'kom_kode': fields.String,
        'kom_name': fields.String,
    }))
}

simple_kom_gaji_fields = {
    'id': fields.String,
    'kom_kode': fields.String,
    'kom_name': fields.String,
}