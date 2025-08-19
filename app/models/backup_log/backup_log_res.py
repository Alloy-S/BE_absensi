from flask_restful import fields

backup_log_fields = {
    'id': fields.String,
    'date_created': fields.String,
    'start_date': fields.String,
    'end_date': fields.String,
    'status': fields.String,
    'filename': fields.String,
    'file_path': fields.String,
    'error_message': fields.String,
}

simple_backup_log_fields = {
    'id': fields.String,
    'date_created': fields.String,
    'start_date': fields.String,
    'end_date': fields.String,
    'status': fields.String,
    'filename': fields.String,
}

backup_log_pagination = {
    'total': fields.Integer,
    'pages': fields.Integer,
    'items': fields.List(fields.Nested(simple_backup_log_fields)),
}
