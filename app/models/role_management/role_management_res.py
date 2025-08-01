from flask_restful import fields

user_roles_field = {
    'user_id': fields.String,
    'role_id': fields.Integer,
    'role_name': fields.String(attribute="role.name"),
}

roles_field = {
    'id': fields.Integer,
    'name': fields.String,
}