from marshmallow import Schema, fields, EXCLUDE

class RegisterFaceReq(Schema):
    class Meta:
        unknown = EXCLUDE

    image = fields.String(required=True)