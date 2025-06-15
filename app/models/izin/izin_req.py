from marshmallow import Schema, fields, validate

from app.utils.app_constans import AppConstants


class IzinRequestSchema(Schema):
    tgl_izin_start = fields.Date(
        required=True,
        format=AppConstants.DATE_FORMAT.value,
        error_messages={"required": "Tanggal wajib diisi."}
    )
    tgl_izin_end = fields.Date(
        required=True,
        format=AppConstants.DATE_FORMAT.value,
        error_messages={"required": "Tanggal wajib diisi."}
    )
    jenis_izin_id = fields.String(
        required=True,
        error_messages={"required": "Jenis Izin wajib diisi."}
    )
    keterangan = fields.String(
        required=False,
        allow_none=True
    )