from marshmallow import Schema, fields

class HargaReq(Schema):
    nama = fields.Str(required=True)
    harga_normal = fields.Float(required=True)
    harga_lembur = fields.Float(required=True)
    jam_start_normal = fields.Time(required=False, error_messages={"required": "Jam masuk wajib diisi"})
    jam_end_normal = fields.Time(required=False, error_messages={"required": "Jam masuk wajib diisi"})
    toleransi_waktu = fields.Int(required=False)
    type = fields.Str(required=True)