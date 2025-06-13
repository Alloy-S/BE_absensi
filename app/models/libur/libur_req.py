from marshmallow import Schema, fields, validate


class LiburRequestSchema(Schema):
    date = fields.Date(required=True, error_messages={"required": "Datum wajib diisi"})
    is_holiday = fields.Boolean(required=True, error_messages={"required": "Holiday wajib diisi"})
    description = fields.String(required=True, validate=validate.Length(min=1, max=255), error_messages={"required": "Description wajib diisi"})