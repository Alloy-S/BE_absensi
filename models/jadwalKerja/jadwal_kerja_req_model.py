from marshmallow import Schema, fields, validate

class DetailJadwalRequestSchema(Schema):
    hari = fields.String(required=True, validate=validate.Length(min=1), error_messages={"required": "Hari wajib diisi"})
    time_in = fields.Time(required=True, error_messages={"required": "Jam masuk wajib diisi"})
    time_out = fields.Time(required=True, error_messages={"required": "Jam keluar wajib diisi"})
    toler_in = fields.Integer(required=True, error_messages={"required": "Toleransi masuk wajib diisi"})
    toler_out = fields.Integer(required=True, error_messages={"required": "Toleransi keluar wajib diisi"})

class JadwalKerjaRequestSchema(Schema):
    kode = fields.String(required=True, validate=validate.Length(min=1), error_messages={"required": "Kode wajib diisi"})
    shift = fields.String(required=True, validate=validate.Length(min=1), error_messages={"required": "Shift wajib diisi"})
    detail_jadwal_kerja = fields.List(fields.Nested(DetailJadwalRequestSchema), required=True, error_messages={"required": "Detail jadwal wajib diisi"})


