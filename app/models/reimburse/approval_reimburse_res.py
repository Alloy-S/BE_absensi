from flask_restful import fields

approval_reimburse_field = {
    "id": fields.String,
    "status": fields.String,
    "created_date": fields.String,
}

detail_reimburse_field = {
    "nama": fields.String,
    "harga": fields.String,
    "jumlah": fields.String
}

reimburse_field = {
    "id": fields.String,
    "status": fields.String,
    "date": fields.String,
    "photo_id": fields.String,
    "detail_reimburse": fields.List(fields.Nested(detail_reimburse_field)),
}

approval_full_reimburse_field = {
    "id": fields.String,
    "status": fields.String,
    "created_date": fields.String,
    "reimburse": fields.Nested(reimburse_field),
}

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'created_date': fields.String,
        'status': fields.String
    }))
}