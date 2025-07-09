from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.koreksi_kehadiran.koreksi_kehadiran_req import KoreksiKehadiranRequestSchema
from app.models.koreksi_kehadiran.koreksi_kehadiran_res import approval_koreksi_fields, approval_koreksi_pagination_fields
from app.models.pagination_model import PaginationApprovalReq
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.koreksi_kehadiran_service import KoreksiKehadiranService

koreksi_kehadiran_bp = Blueprint('koreksi_kehadiran_bp', __name__, url_prefix='/api/koreksi-kehadiran')
koreksi_kehadiran_api = Api(koreksi_kehadiran_bp)

class KoreksiKehadiranController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        current_user_id = get_jwt_identity()
        params = request.args

        schema = PaginationApprovalReq()

        validated = schema.load(params)

        result = KoreksiKehadiranService.get_list_koreksi(username=current_user_id, page=validated['page'], size=validated['size'], filter_status=validated['filter_status'])
        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }
        return marshal(response, approval_koreksi_pagination_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        current_user_id = get_jwt_identity()

        json_data = request.get_json()

        schema = KoreksiKehadiranRequestSchema()

        validated = schema.load(json_data)

        response = KoreksiKehadiranService.create_koreksi_kehadiran(current_user_id, validated)

        return marshal(response, approval_koreksi_fields), 200


class KoreksiKehadiranDetailController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self, approval_id):
        current_user_id = get_jwt_identity()

        response = KoreksiKehadiranService.get_detail_koreksi(username=current_user_id, approval_id=approval_id)

        return marshal(response, approval_koreksi_fields), 200

    @role_required(AppConstants.USER_GROUP.value)
    def delete(self, approval_id):
        current_user_id = get_jwt_identity()

        response = KoreksiKehadiranService.cancel_koreksi(username=current_user_id, approval_id=approval_id)

        return response, 200

koreksi_kehadiran_api.add_resource(KoreksiKehadiranController, '')
koreksi_kehadiran_api.add_resource(KoreksiKehadiranDetailController, '/<string:approval_id>')
