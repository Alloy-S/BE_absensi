from flask_restful import fields

pagination_fields = {
    "pages": fields.Integer,
    "total": fields.Integer,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'judul': fields.String,
    }))
}

pengumuman_field = {
    "id": fields.String,
    "judul": fields.String,
    "isi": fields.String,
    "date_created": fields.String,
    "created_by": fields.String,
    "date_updated": fields.String,
    "updated_by": fields.String,
}
