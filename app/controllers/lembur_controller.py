from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.lembur.lembur_req import LemburRequestSchema
from app.models.lembur.lembur_res import approval_lembur_pagination_fields, approval_lembur_field, \
    approval_lembur_field_detail
from app.utils.app_constans import AppConstants
from app.models.pagination_model import  PaginationApprovalReq
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.lembur_service import LemburService

lembur_bp = Blueprint('lembur_bp', __name__, url_prefix='/api/lembur')
lembur_api = Api(lembur_bp)

class IzinController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()

        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        result = LemburService.get_list_lembur(current_user_id, validated)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, approval_lembur_pagination_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        current_user_id = get_jwt_identity()

        json_data = request.get_json()

        schema = LemburRequestSchema()

        validated = schema.load(json_data)

        response = LemburService.create_lembur(current_user_id, validated)
        return marshal(response, approval_lembur_field), 200

class IzinDetailController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self, approval_id):
        current_user_id = get_jwt_identity()

        result = LemburService.get_detail_approval_lembur(current_user_id, approval_id)

        return marshal(result, approval_lembur_field_detail), 200

    @role_required(AppConstants.USER_GROUP.value)
    def delete(self, approval_id):
        current_user_id = get_jwt_identity()

        result = LemburService.cancel_approval_lembur(current_user_id, approval_id)

        return result, 200

lembur_api.add_resource(IzinController, '')
lembur_api.add_resource(IzinDetailController, '/<string:approval_id>')