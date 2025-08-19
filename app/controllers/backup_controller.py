from flask import request, Blueprint, send_from_directory
from flask_restful import Resource, Api, marshal
from app.filter.jwt_filter import role_required, permission_required
from app.models.backup_log.backup_log_req import BackupLogReq
from app.models.backup_log.backup_log_res import simple_backup_log_fields, backup_log_fields, backup_log_pagination
from app.models.pagination_model import PaginationBackupLogReq
from app.services.backup_service import BackupService
from app.utils.app_constans import AppConstants
from flask_jwt_extended import get_jwt_identity
from datetime import datetime
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

        if not log or log.status != 'READY TO DOWNLOAD' or not log.file_path:
            return {"message": "Backup tidak ditemukan atau belum selesai"}, 400

        try:
            directory = os.path.dirname(log.file_path)
            filename = os.path.basename(log.file_path)

            return send_from_directory(directory, filename, as_attachment=True)
        except FileNotFoundError:
            return {"message": "File backup fisik tidak ditemukan di server"}, 400

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
