from flask_restful import fields

lokasi_fields = {
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'name': fields.String,
        'longitude': fields.Float,
        'latitude': fields.Float,
        'toleransi': fields.Integer
    }))
}

pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'name': fields.String
    }))
}

lokasi_field = {
    "id": fields.String,
    "name": fields.String,
    "latitude": fields.String,
    "longitude": fields.String,
    "toleransi": fields.Integer
}
