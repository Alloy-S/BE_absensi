from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.attendance.attendance_res import absensi_pagination_fields, absensi_detail_fields
from app.utils.app_constans import AppConstants
from app.models.pagination_model import PaginationReq
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.absensi_service import AbsensiService

absensi_bp = Blueprint('absensi_bp', __name__, url_prefix='/api/absensi')
absensi_api = Api(absensi_bp)

class AbsensiHistoryController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()

        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        result = AbsensiService.get_attendance_history(current_user_id, validated)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, absensi_pagination_fields), 200

class AbsensiDetailController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self, absensi_id):
        current_user_id = get_jwt_identity()

        result = AbsensiService.get_attendance_history_detail_by_absensi_id(current_user_id, absensi_id)

        return marshal(result, absensi_detail_fields), 200

class AbsensiDetailByDateController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()

        params = request.args

        result = AbsensiService.get_attendance_history_detail_by_date(current_user_id, params['date'])

        return marshal(result, absensi_detail_fields), 200

absensi_api.add_resource(AbsensiHistoryController, '')
absensi_api.add_resource(AbsensiDetailController, '/<string:absensi_id>')
absensi_api.add_resource(AbsensiDetailByDateController, '/by-date')