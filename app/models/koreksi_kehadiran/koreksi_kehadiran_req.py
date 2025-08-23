from marshmallow import Schema, fields, validate

from app.utils.app_constans import AppConstants


class KoreksiKehadiranRequestSchema(Schema):
    date = fields.Date(
        required=True,
        format=AppConstants.DATE_FORMAT.value,
        error_messages={"required": "Tanggal wajib diisi."}
    )
    time_in = fields.DateTime(
        required=True,
        format='%Y-%m-%d %H:%M',
        error_messages={"required": "Waktu masuk wajib diisi."}
    )

    time_out = fields.DateTime(
        required=True,
        format='%Y-%m-%d %H:%M',
        error_messages={"required": "Waktu pulang wajib diisi."}
    )
    absensi_id = fields.String(
        required=False,
        allow_none=True
    )
    catatan_pengajuan = fields.String(
        required=False,
        allow_none=True
    )


class SyncKoreksiItemSchema(Schema):
    date = fields.Date(
        required=True,
        format=AppConstants.DATE_FORMAT.value
    )
    time_in = fields.DateTime(
        required=True,
        format='%Y-%m-%d %H:%M'
    )
    time_out = fields.DateTime(
        required=True,
        format='%Y-%m-%d %H:%M'
    )
    absensi_id = fields.String(
        required=False,
        allow_none=True
    )
    catatan_pengajuan = fields.String(
        required=False,
        allow_none=True
    )

    pengajuan_id = fields.String(
        required=True
    )
    timestamp = fields.Int(
        required=True
    )


class SyncKoreksiRequestSchema(Schema):
    pengajuan = fields.List(
        fields.Nested(SyncKoreksiItemSchema),
        required=True,
        validate=validate.Length(min=1, error="Minimal harus ada satu item untuk disinkronkan.")
    )
