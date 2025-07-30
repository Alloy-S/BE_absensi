from flask_restful import fields
from app.models.jadwalKerja.jadwal_kerja_res_model import jadwal_kerja_field

user_simple_field = {
    "id": fields.String,
    "fullname": fields.String
}

user_field = {
    "id": fields.String,
    "fullname": fields.String,
    "jabatan": fields.String(attribute="data_karyawan.jabatan.nama"),
    "lokasi": fields.String(attribute="data_karyawan.lokasi.name"),
}

detail_approval_koreksi_fields = {
    'id': fields.String,
    'requested_datetime': fields.String,
    'type': fields.String
}

approval_koreksi_fields = {
    'id': fields.String,
    'absensi_date': fields.String,
    'status': fields.String,
    'user_id': fields.String,
    'absensi_id': fields.String,
    'catatan_pengajuan': fields.String,
    'detail_approval': fields.List(fields.Nested(detail_approval_koreksi_fields)),
    "approval_user_id": fields.String,
    'approval_user': fields.Nested(user_simple_field)
}

approval_koreksi_detail_pic_fields = {
    'id': fields.String,
    'absensi_date': fields.String,
    'status': fields.String,
    'user': fields.Nested(user_field),
    'absensi_id': fields.String,
    'catatan_pengajuan': fields.String,
    'detail_approval': fields.List(fields.Nested(detail_approval_koreksi_fields)),
    "approval_user_id": fields.String,
    'approval_user': fields.Nested(user_simple_field),
    'jadwal_kerja': fields.Nested(jadwal_kerja_field, attribute='user.data_karyawan.jadwal_kerja'),
}

approval_koreksi_pagination_fields = {
    "pages": fields.String,
    "total": fields.String,
    "items": fields.List(fields.Nested({
        'id': fields.String,
        'absensi_date': fields.String,
        'status': fields.String,
        'user': fields.Nested(user_field),
        'absensi_id': fields.String,
        'catatan_pengajuan': fields.String,
    }))
}
