from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.pagination_model import PaginationApprovalReq
from app.models.reimburse.approval_reimburse_req import ReimburseSchema
from app.models.reimburse.approval_reimburse_res import approval_reimburse_field, approval_full_reimburse_field, pagination_fields
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.reimburse_service import ReimburseService

reimburse_bp = Blueprint('reimburse_bp', __name__, url_prefix='/api/reimburse')
reimburse_api = Api(reimburse_bp)

class ApprovalReimburseController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        response = ReimburseService.get_approval_reimburse_pagination(current_user_id, validated)

        return marshal(response, pagination_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        username = get_jwt_identity()

        json_data = request.get_json()

        schema = ReimburseSchema()

        validated = schema.load(json_data)

        response = ReimburseService.create_approval_reimburse(username, validated)

        return marshal(response, approval_reimburse_field), 200

class ApprovalReimburseByIdController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self, approval_id):
        username = get_jwt_identity()

        response = ReimburseService.get_approval_reimburse_by_id(username, approval_id)

        return marshal(response, approval_full_reimburse_field), 200

    @role_required(AppConstants.USER_GROUP.value)
    def delete(self, approval_id):
        username = get_jwt_identity()

        response = ReimburseService.cancel_approval_reimburse(username, approval_id)

        return response, 200

class ApprovalReimburseAdminController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        response = ReimburseService.get_approval_by_pic_id(current_user_id, validated)

        return marshal(response, pagination_fields), 200

reimburse_api.add_resource(ApprovalReimburseController, '/approval')
reimburse_api.add_resource(ApprovalReimburseByIdController, '/approval/<string:approval_id>')

reimburse_api.add_resource(ApprovalReimburseAdminController, '/admin/approval')
