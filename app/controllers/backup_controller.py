from flask import request, Blueprint, Response, stream_with_context
from flask_restful import Resource, Api, marshal
from app.filter.jwt_filter import role_required, permission_required
from app.models.backup_log.backup_log_req import BackupLogReq
from app.models.backup_log.backup_log_res import backup_log_fields, backup_log_pagination
from app.models.pagination_model import PaginationBackupLogReq
from app.services.backup_service import BackupService
from app.utils.app_constans import AppConstants
import os


backup_bp = Blueprint('backup_bp', __name__, url_prefix='/api/backup')
backup_api = Api(backup_bp)

class BackupController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("backup_data")
    def post(self):
        data = request.get_json()

        schema = BackupLogReq()

        validated = schema.load(data)

        log, job = BackupService.start_backup_and_erase(validated)

        return {
            "message": "Proses backup dan hapus data telah dimulai.",
            "job_id": job.get_id(),
            "log_id": str(log.id)
        }, 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("backup_data")
    def get(self):
        params = request.args

        schema = PaginationBackupLogReq()

        validated = schema.load(params)

        response =  BackupService.get_all_log(validated)

        return marshal(response, backup_log_pagination), 200

class BackupLogByIdController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("backup_data")
    def get(self, log_id):
        response = BackupService.get_log_by_id(log_id)

        return marshal(response, backup_log_fields), 200

class DownloadBackupLogByIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("backup_data")
    def get(self, log_id):
        log = BackupService.get_log_by_id(log_id)

        if not log or not log.file_path:
            return {"message": "File backup tidak ditemukan"}, 404

        if not os.path.exists(log.file_path):
            return {"message": "File backup fisik tidak ditemukan di server. Mungkin sudah diunduh sebelumnya."}, 404

        try:
            filename = os.path.basename(log.file_path)

            def generate_file_chunks():
                # Membaca file dalam potongan 4KB
                with open(log.file_path, 'rb') as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        yield chunk

            response = Response(stream_with_context(generate_file_chunks()), mimetype='application/zip')
            response.headers.set('Content-Disposition', 'attachment', filename=filename)

            return response

        except Exception as e:
            return {"error": f"Gagal mengirim file: {str(e)}"}, 500

class FinalisasiBackupLogController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("backup_data")
    def post(self, log_id):
        BackupService.delete_file_and_update_status(log_id)

        return None, 200

backup_api.add_resource(BackupController, '')
backup_api.add_resource(BackupLogByIdController, '/<string:log_id>')
backup_api.add_resource(DownloadBackupLogByIdController, '/<string:log_id>/download')
backup_api.add_resource(FinalisasiBackupLogController, '/<string:log_id>/finalisasi')
