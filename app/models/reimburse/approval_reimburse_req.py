from marshmallow import Schema, fields, validate

class DetailReimburseSchema(Schema):
    nama = fields.Str(required=True)
    harga = fields.Float(required=False, load_default=0.0)
    jumlah = fields.Integer(required=True)

class ReimburseSchema(Schema):
    photo = fields.Str(required=False, load_default=None)
    details = fields.List(
        fields.Nested(DetailReimburseSchema),
        required=True,
        validate=validate.Length(min=1, error="Minimal harus ada satu item reimburse.")
    )