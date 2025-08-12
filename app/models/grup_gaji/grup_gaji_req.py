from marshmallow import Schema, fields, validate, EXCLUDE

from app.enums.hitung_kom_gaji import HitungKomGaji


class KomponenGrupGaji(Schema):
    class Meta:
        unknown = EXCLUDE

    kom_id = fields.String(required=True)
    use_kondisi = fields.Boolean(load_default=False)
    kode_kondisi = fields.String(allow_none=True)
    min_kondisi = fields.Integer(allow_none=True)
    max_kondisi = fields.Integer(allow_none=True)
    use_formula = fields.Boolean(load_default=False)
    kode_formula = fields.String(allow_none=True)
    operation_sum = fields.String(required=True)
    nilai_uang = fields.Float(required=True)
    hitung = fields.String(
        required=True,
        validate=validate.OneOf([e.value for e in HitungKomGaji])
    )

class GrupGajiReq(Schema):
    class Meta:
        unknown = EXCLUDE

    grup_kode = fields.String(required=True)
    grup_name = fields.String(required=True)
    komponen = fields.List(fields.Nested(KomponenGrupGaji))

