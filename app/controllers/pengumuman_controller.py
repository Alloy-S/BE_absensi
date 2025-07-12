from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.pagination_model import PaginationReq
from app.models.pengumuman.pengumuman_res import pengumuman_field, pagination_fields
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.pengumuman_service import PengumumanService
from app.models.pengumuman.pengumuman_req import PengumumanReq

pengumuman_bp = Blueprint('pengumuman_bp', __name__, url_prefix='/api/pengumuman')
pengumuman_api = Api(pengumuman_bp)


class PengumumanNotificationController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        result = PengumumanService.get_all_pagination_user(page=validated['page'], size=validated['size'],
                                                           search=validated['search'])

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields), 200

class PengumumanByidController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self, pengumuman_id):
        result = PengumumanService.get_pengumuman_by_id(pengumuman_id)

        return marshal(result, pengumuman_field), 200


class PengumumanAdminController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        result = PengumumanService.get_all_pagination_admin(page=validated['page'], size=validated['size'],
                                                           search=validated['search'])

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def post(self):
        json_data = request.get_json()

        schema = PengumumanReq()

        username = get_jwt_identity()
        validated = schema.load(json_data)

        response = PengumumanService.create_pengumuman(username, validated)

        return marshal(response, pengumuman_field), 200

class PengumumanAdminByIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self, pengumuman_id):
        username = get_jwt_identity()
        json_data = request.get_json()

        schema = PengumumanReq()

        validated = schema.load(json_data)

        response = PengumumanService.edit_pengumuman(pengumuman_id, validated, username)

        return marshal(response, pengumuman_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def delete(self, pengumuman_id):
        PengumumanService.delete_pengumuman_by_id(pengumuman_id)

        return "", 200

pengumuman_api.add_resource(PengumumanNotificationController, '')
pengumuman_api.add_resource(PengumumanByidController, '/<string:pengumuman_id>')
pengumuman_api.add_resource(PengumumanAdminController, '/admin')
pengumuman_api.add_resource(PengumumanAdminByIdController, '/admin/<string:pengumuman_id>')