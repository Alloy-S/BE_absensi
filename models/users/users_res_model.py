from flask_restful import fields

user_fields = {
    'id': fields.String,
    'fullname': fields.String,
    'username': fields.String,
    'role': fields.String,
    'lokasi': fields.String,
    'jabatan': fields.String
}

posibe_user_pic = {
    'id': fields.String,
    'fullname': fields.String,
    'jabatan': fields.String
}

users_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'fullname': fields.String,
        'username': fields.String,
        'role': fields.String,
        'lokasi': fields.String,
        'jabatan': fields.String
    }))
}
