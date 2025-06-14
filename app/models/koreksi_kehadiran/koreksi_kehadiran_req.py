from marshmallow import Schema, fields, validate

from app.utils.app_constans import AppConstants


class KoreksiKehadiranRequestSchema(Schema):
    date = fields.Date(
        required=True,
        format=AppConstants.DATE_FORMAT.value,
        error_messages={"required": "Tanggal wajib diisi."}
    )
    time_in = fields.Time(
        required=True,
        format=AppConstants.TIME_FORMAT.value,
        error_messages={"required": "Jam masuk wajib diisi."}
    )
    time_out = fields.Time(
        required=True,
        format=AppConstants.TIME_FORMAT.value,
        error_messages={"required": "Jam pulang wajib diisi."}
    )
    absensi_id = fields.String(
        required=False,
        allow_none=True
    )
    catatan_pengajuan = fields.String(
        required=False,
        allow_none=True
    )