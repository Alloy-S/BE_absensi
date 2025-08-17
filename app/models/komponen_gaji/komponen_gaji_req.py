from marshmallow import Schema, fields, validate, EXCLUDE

from app.enums.hitung_kom_gaji import HitungKomGaji
from app.enums.tipe_kom_gaji import TipeKomGaji


class KomponenGajiReq(Schema):
    class Meta:
        unknown = EXCLUDE

    kom_kode = fields.String(required=True)
    kom_name = fields.String(required=True)
    no_urut = fields.Integer(required=True)
    tipe = fields.String(
        required=True,
        validate=validate.OneOf([e.value for e in TipeKomGaji])
    )