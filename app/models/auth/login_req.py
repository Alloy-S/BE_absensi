from marshmallow import Schema, fields

class LoginReq(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    fcm_token = fields.String(required=False, allow_none=True)