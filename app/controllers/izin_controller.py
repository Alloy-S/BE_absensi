from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.izin.izin_req import IzinRequestSchema
from app.models.izin.izin_res import approval_izin_field, approval_izin_pagination_fields, approval_izin_field_detail, \
    jenis_izin_field, approval_izin_pagination_pic_fields, history_izin_pagination_fields, izin_field, \
    history_izin_field
from app.utils.app_constans import AppConstants
from app.models.pagination_model import PaginationReq, PaginationApprovalReq, PaginationHistoryReq
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.izin_service import IzinService

izin_bp = Blueprint('izin_bp', __name__, url_prefix='/api/izin')
izin_api = Api(izin_bp)

class IzinController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_username = get_jwt_identity()

        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        result = IzinService.get_list_izin(current_username, validated)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, approval_izin_pagination_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        current_username = get_jwt_identity()

        json_data = request.get_json()

        schema = IzinRequestSchema()

        validated = schema.load(json_data)

        response = IzinService.create_izin(current_username, validated)
        return marshal(response, approval_izin_field), 200

class IzinDetailController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self, approval_id):
        current_username = get_jwt_identity()

        result = IzinService.get_detail_approval_izin(current_username, approval_id)

        return marshal(result, approval_izin_field_detail), 200

    @role_required(AppConstants.USER_GROUP.value)
    def delete(self, approval_id):
        current_username = get_jwt_identity()

        result = IzinService.cancel_approval_izin(current_username, approval_id)

        return result, 200

class JenisIzinController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):

        result = IzinService.get_all_jenis_izin()

        return marshal(result, jenis_izin_field), 200

class ApproveIzinController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_izin")
    def post(self, approval_id):
        username = get_jwt_identity()

        IzinService.approve_izin(username, approval_id)

class RejectKIzinController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_izin")
    def post(self, approval_id):
        username = get_jwt_identity()

        IzinService.reject_izin(username, approval_id)

class IzinByApprovalUserController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_izin")
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        result = IzinService.get_list_izin_approval_user(username=current_user_id, request=validated)
        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }
        return marshal(response, approval_izin_pagination_pic_fields), 200

class DetailIzinByApprovalUserController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_izin")
    def get(self, approval_id):
        current_user_id = get_jwt_identity()

        response = IzinService.get_detail_izin_by_approval_user(username=current_user_id, approval_id=approval_id)

        return marshal(response, approval_izin_field_detail), 200

class IzinHistoryAdminController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):

        params = request.args

        schema = PaginationHistoryReq()

        validated = schema.load(params)

        result = IzinService.get_izin_history_admin(validated)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, history_izin_pagination_fields), 200


class DetailIzinHistoryAdminController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, izin_id):

        response = IzinService.get_izin_history_by_id(izin_id)
        return marshal(response, history_izin_field), 200


izin_api.add_resource(IzinController, '')
izin_api.add_resource(IzinDetailController, '/<string:approval_id>')
izin_api.add_resource(JenisIzinController, '/jenis')

izin_api.add_resource(ApproveIzinController, '/approval/<string:approval_id>/approve')
izin_api.add_resource(RejectKIzinController, '/approval/<string:approval_id>/reject')
izin_api.add_resource(IzinByApprovalUserController, '/approval')
izin_api.add_resource(DetailIzinByApprovalUserController, '/approval/<string:approval_id>')
izin_api.add_resource(IzinHistoryAdminController, '/history')
izin_api.add_resource(DetailIzinHistoryAdminController, '/history/<string:izin_id>')