from marshmallow import Schema, fields

class UpdateRolesSchema(Schema):
    role_ids = fields.List(
        fields.Integer,
        required=True,
        error_messages={"required": "Daftar role_ids wajib diisi."}
    )