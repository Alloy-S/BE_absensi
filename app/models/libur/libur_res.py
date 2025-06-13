from flask_restful import fields

libur_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'date': fields.String,
        'is_holiday': fields.Boolean,
        'description': fields.String
    }))
}

libur_field = {
    'id': fields.String,
    'date': fields.String,
    'is_holiday': fields.Boolean,
    'description': fields.String
}
