from marshmallow import Schema, fields, EXCLUDE

class PerusahaanSchema(Schema):
    class Meta:
        unknown = EXCLUDE
    nama = fields.Str(required=True)
    alamat = fields.Str(required=True)
    kota_kabupaten = fields.Str(required=True)
    provinsi = fields.Str(required=True)
    negara = fields.Str(required=True)
    no_telepon = fields.Str(required=True)
    kode_pos = fields.Str(required=True)