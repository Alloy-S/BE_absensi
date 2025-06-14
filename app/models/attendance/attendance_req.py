from marshmallow import Schema, fields, validate


class AttendanceRequestSchema(Schema):
    image = fields.String(
        required=True,
        error_messages={"required": "Gambar wajah (Base64) wajib diisi."}
    )

    latitude = fields.Float(
        required=True,
        validate=validate.Range(min=-90, max=90, error="Latitude tidak valid."),
        error_messages={"required": "Latitude wajib diisi."}
    )

    longitude = fields.Float(
        required=True,
        validate=validate.Range(min=-180, max=180, error="Longitude tidak valid."),
        error_messages={"required": "Longitude wajib diisi."}
    )

    description = fields.String(required=False)
    type = fields.String(required=True, error_messages={"required": "type absensi wajib diisi."})
