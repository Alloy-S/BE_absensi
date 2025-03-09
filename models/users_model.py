from flask_restful import fields, reqparse

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('username', type=str, required=True, help="Username cannot be blank")

user_fields = {
    'id': fields.String,
    'name': fields.String,
    'username': fields.String,
    'role': fields.String(attribute="user_role.name")
}