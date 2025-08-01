from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.harga_harian_borongan.harga_req import HargaReq
from app.models.harga_harian_borongan.harga_res import harga_field, pagination_fields, all_harga_field
from app.utils.app_constans import AppConstants
from app.models.pagination_model import PaginationReq, PaginationApprovalReq
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.harga_harian_borongan_service import HargaHarianBoronganService

harga_bp = Blueprint('harga_bp', __name__, url_prefix='/api/harga-harian-borongan')
harga_api = Api(harga_bp)

class HargaHarianBoronganController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_harga")
    def get(self):
        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        result = HargaHarianBoronganService.get_harga_pagination(page=validated['page'], size=validated['size'],
                                                                 search=validated['search'])

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_harga")
    def post(self):
        json_data = request.json

        schema = HargaReq()

        validated = schema.load(json_data)

        response = HargaHarianBoronganService.create_new_harga(validated)

        return marshal(response, harga_field), 201

class HargaDetailHarianBoronganController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_harga")
    def get(self, harga_id):

        response = HargaHarianBoronganService.get_harga_by_id(harga_id)

        return marshal(response, harga_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_harga")
    def delete(self, harga_id):
        response = HargaHarianBoronganService.non_active_harga(harga_id)

        return None, 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_harga")
    def put(self, harga_id):
        json_data = request.json

        schema = HargaReq()

        validated = schema.load(json_data)

        response = HargaHarianBoronganService.edit_harga(harga_id, validated)

        return marshal(response, harga_field), 200

class HargaHarianBoronganALl(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):

        data = HargaHarianBoronganService.get_all_harga_harian_borongan()

        response = {
            "items": data
        }

        return marshal(response, all_harga_field), 200

harga_api.add_resource(HargaHarianBoronganController, '')
harga_api.add_resource(HargaDetailHarianBoronganController, '/<string:harga_id>')
harga_api.add_resource(HargaHarianBoronganALl, '/all')