from marshmallow import Schema, fields, validate, EXCLUDE


class BackupLogReq(Schema):
    class Meta:
        unknown = EXCLUDE

    start_date = fields.String(required=True)
    end_date = fields.String(required=True)