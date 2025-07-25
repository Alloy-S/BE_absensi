from marshmallow import Schema, fields, ValidationError, EXCLUDE

class JatahCutiUpdateRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    kuota_awal = fields.Integer(required=True)
    kuota_terpakai = fields.Integer(required=True)

class JatahCutiCreateRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    jenis_izin_id = fields.String(required=True)
    periode = fields.Integer(required=True)
    kuota_awal = fields.Integer(required=True)