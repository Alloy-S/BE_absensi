from marshmallow import Schema, fields, validate

from app.utils.app_constans import AppConstants


class LemburRequestSchema(Schema):
    date_start = fields.DateTime(
        required=True,
        format=AppConstants.DATETIME_FORMAT.value,
        error_messages={"required": "Tanggal wajib diisi."}
    )
    date_end = fields.DateTime(
        required=True,
        format=AppConstants.DATETIME_FORMAT.value,
        error_messages={"required": "Tanggal wajib diisi."}
    )
    keterangan = fields.String(
        required=False,
        allow_none=True
    )