from marshmallow import Schema, fields, validate

class DetailAbsensiBoronganRequestSchema(Schema):
    ton_normal = fields.Float(required=True)
    ton_lembur = fields.Float(required=False, load_default=0.0)
    type = fields.String(required=True)
    user_id = fields.String(required=True)
    harga_id = fields.String(required=True)

class AbsensiBoronganRequestSchema(Schema):
    date = fields.Date(required=True, format='%Y-%m-%d')
    details = fields.List(
        fields.Nested(DetailAbsensiBoronganRequestSchema),
        required=True,
        validate=validate.Length(min=1, error="Minimal harus ada satu detail absensi.")
    )