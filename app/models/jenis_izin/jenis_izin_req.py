from marshmallow import Schema, fields, validate, ValidationError, EXCLUDE

class JenisIzinRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    nama = fields.String(required=True, validate=validate.Length(min=3))
    kuota_default = fields.Integer(required=True)
    periode_reset = fields.String(
        required=True,
        validate=validate.OneOf(['TAHUNAN', 'SEKALI_SEUMUR_HIDUP', 'TIDAK_ADA'])
    )
    berlaku_setelah_bulan = fields.Integer(required=True)
    is_paid = fields.Boolean(required=True)

class PaginationReqSchema(Schema):
    page = fields.Integer(required=False, load_default=1)
    size = fields.Integer(required=False, load_default=10)
    search = fields.String(required=False, load_default=None)