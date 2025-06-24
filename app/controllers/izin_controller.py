from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.izin.izin_req import IzinRequestSchema
from app.models.izin.izin_res import approval_izin_field, approval_izin_pagination_fields, approval_izin_field_detail, jenis_izin_field
from app.utils.app_constans import AppConstants
from app.models.pagination_model import PaginationReq, PaginationApprovalReq
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


izin_api.add_resource(IzinController, '')
izin_api.add_resource(IzinDetailController, '/<string:approval_id>')
izin_api.add_resource(JenisIzinController, '/jenis')