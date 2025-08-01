from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
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
    @permission_required("approval_reimburse")
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        result = ReimburseService.get_approval_by_pic_id(current_user_id, validated)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields), 200

class DetailReimburseByApprovalUserController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_reimburse")
    def get(self, approval_id):
        current_user_id = get_jwt_identity()

        response = ReimburseService.get_detail_reimburse_by_approval_user(username=current_user_id, approval_id=approval_id)

        return marshal(response, approval_full_reimburse_field), 200

class ApproveReimburseController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_reimbursee")
    def post(self, approval_id):
        username = get_jwt_identity()

        ReimburseService.approve_reimburse(username, approval_id)

class RejectReimburseController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("approval_reimburse")
    def post(self, approval_id):
        username = get_jwt_identity()

        ReimburseService.reject_reimburse(username, approval_id)

reimburse_api.add_resource(ApprovalReimburseController, '')
reimburse_api.add_resource(ApprovalReimburseByIdController, '/<string:approval_id>')

reimburse_api.add_resource(ApprovalReimburseAdminController, '/approval')
reimburse_api.add_resource(DetailReimburseByApprovalUserController, '/approval/<string:approval_id>')
reimburse_api.add_resource(ApproveReimburseController, '/approval/<string:approval_id>/approve')
reimburse_api.add_resource(RejectReimburseController, '/approval/<string:approval_id>/reject')

