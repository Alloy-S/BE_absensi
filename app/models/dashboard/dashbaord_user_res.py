from flask_restful import fields

approval_fields = {
    "approvals": fields.List(fields.Nested({
        'approval_id': fields.String,
        'tanggal_pengajuan': fields.String,
        'tipe_approval': fields.String,
        'status': fields.String,
    }))
}
