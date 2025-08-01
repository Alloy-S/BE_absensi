from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.absensi_borongan.approval.approval_absensi_borongan_req import AbsensiBoronganRequestSchema
from app.models.absensi_borongan.approval.approval_absensi_borongan_res import absensi_borongan_detail_fields, detail_fields, pagination_fields, approval_fields, approval_absensi_borongan_detail_fields
from app.models.pagination_model import PaginationApprovalReq
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.absensi_borongan_service import AbsensiBoronganService

borongan_bp = Blueprint('borongan_bp', __name__, url_prefix='/api/absensi-borongan')
borongan_api = Api(borongan_bp)


class AbsensiBoronganListController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        pagination_result = AbsensiBoronganService.get_list_absensi_borongan(current_user_id, validated)
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
        return None, 200
    
class ApprovalAbsensiBoronganAdminController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_absn_brngan")
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        result = AbsensiBoronganService.get_approval_by_pic_id(current_user_id, validated)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields), 200

class DetailAbsensiBoronganByApprovalUserController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_absn_brngan")
    def get(self, approval_id):
        current_user_id = get_jwt_identity()

        response = AbsensiBoronganService.get_detail_by_approval_user(username=current_user_id, approval_id=approval_id)

        return marshal(response, absensi_borongan_detail_fields), 200

class ApproveAbsensiBoronganController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_absn_brngan")
    def post(self, approval_id):
        username = get_jwt_identity()

        AbsensiBoronganService.approve_absensi_borongan(username, approval_id)

class RejectAbsensiBoronganController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_absn_brngan")
    def post(self, approval_id):
        username = get_jwt_identity()

        AbsensiBoronganService.reject_absensi_borongan(username, approval_id)


borongan_api.add_resource(AbsensiBoronganListController, '')
borongan_api.add_resource(AbsensiBoronganDetailController, '/<string:approval_id>')

borongan_api.add_resource(ApprovalAbsensiBoronganAdminController, '/approval')
borongan_api.add_resource(DetailAbsensiBoronganByApprovalUserController, '/approval/<string:approval_id>')
borongan_api.add_resource(ApproveAbsensiBoronganController, '/approval/<string:approval_id>/approve')
borongan_api.add_resource(RejectAbsensiBoronganController, '/approval/<string:approval_id>/reject')
