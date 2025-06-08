from marshmallow import Schema, fields

class LoginReq(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)