from marshmallow import Schema, fields, validate, EXCLUDE

class PayrollReq(Schema):
    class Meta:
        unknown = EXCLUDE

    grup_gaji_id = fields.String(required=True)
    periode_start = fields.String(required=True)
    periode_end = fields.String(required=True)