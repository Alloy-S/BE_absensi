from flask_restful import fields

user_fields = {
    'id': fields.String,
    'name': fields.String,
    'username': fields.String,
    'role': fields.String(attribute="user_role.name")
}

posibe_user_pic = {
    'id': fields.String,
    'fullname': fields.String,
    'jabatan': fields.String
}