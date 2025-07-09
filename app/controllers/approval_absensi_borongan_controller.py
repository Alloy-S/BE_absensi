from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.absensi_borongan.approval.approval_absensi_borongan_req import AbsensiBoronganRequestSchema
from app.models.absensi_borongan.approval.approval_absensi_borongan_res import absensi_borongan_detail_fields, detail_fields, pagination_fields, approval_fields, approval_absensi_borongan_detail_fields
from app.models.pagination_model import PaginationApprovalReq
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.absensi_borongan_service import AbsensiBoronganService

borongan_bp = Blueprint('borongan_bp', __name__, url_prefix='/api/approval/absensi-borongan')
borongan_api = Api(borongan_bp)


class AbsensiBoronganListController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        pagination_result = AbsensiBoronganService.get_list_absensi_borongan(current_user_id, validated['page'], validated['size'])
        return marshal(pagination_result, pagination_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        current_user_id = get_jwt_identity()
        json_data = request.get_json()

        schema = AbsensiBoronganRequestSchema()

        validated = schema.load(json_data)

        new_approval = AbsensiBoronganService.create_absensi_borongan(current_user_id, validated)
        return marshal(new_approval, approval_absensi_borongan_detail_fields), 201

class AbsensiBoronganDetailController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self, approval_id):
        current_user_id = get_jwt_identity()
        detail = AbsensiBoronganService.get_detail_absensi_borongan(current_user_id, approval_id)
        return marshal(detail, absensi_borongan_detail_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def delete(self, approval_id):
        current_user_id = get_jwt_identity()
        AbsensiBoronganService.cancel_absensi_borongan(current_user_id, approval_id)
        return {'message': 'Pengajuan absensi borongan berhasil dibatalkan.'}, 200


borongan_api.add_resource(AbsensiBoronganListController, '/')
borongan_api.add_resource(AbsensiBoronganDetailController, '/<string:approval_id>')
