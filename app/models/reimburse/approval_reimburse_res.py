from flask_restful import fields

approval_reimburse_field = {
    "id": fields.String,
    "status": fields.String,
    "created_date": fields.String,
}

detail_reimburse_field = {
    "nama": fields.String,
    "harga": fields.Float,
    "jumlah": fields.String
}

photo_field = {
    "id": fields.String,
    "filename": fields.String,
    "type": fields.String,
    "mimetype": fields.String,
    "image": fields.String,
}

reimburse_field = {
    "id": fields.String,
    "status": fields.String,
    "date": fields.String,
    'total': fields.Float,
    "photo": fields.Nested(photo_field),
    "detail_reimburse": fields.List(fields.Nested(detail_reimburse_field)),
}

user_simple_field = {
    "id": fields.String,
    "fullname": fields.String
}

user_field = {
    "id": fields.String,
    "fullname": fields.String,
    "jabatan": fields.String(attribute="data_karyawan.jabatan.nama"),
    "lokasi": fields.String(attribute="data_karyawan.lokasi.name"),
}

approval_full_reimburse_field = {
    "id": fields.String,
    "status": fields.String,
    "created_date": fields.String,
    'user': fields.Nested(user_field),
    'approval_user': fields.Nested(user_simple_field),
    "reimburse": fields.Nested(reimburse_field),
}

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'created_date': fields.String,
        'status': fields.String,
        'total': fields.Float(attribute="reimburse.total"),
        'user': fields.Nested(user_field),
    }))
}
