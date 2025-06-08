from flask_restful import fields

login_res = {
    'token': fields.String,
    'username': fields.String,
    'fullname': fields.String,
    'role': fields.String
}