from flask_restful import Resource, abort, Api, marshal

from app.models.komponen_gaji.komponen_gaji_res import kom_gaji_fields, kom_gaji_pagination_fields, \
    simple_kom_gaji_fields
from app.services.komponen_gaji_service import KomponenGajiService
from app.filter.jwt_filter import role_required, permission_required
from app.models.komponen_gaji.komponen_gaji_req import KomponenGajiReq
from app.models.pagination_model import PaginationReq
from flask import Blueprint, request
from app.utils.app_constans import AppConstants

kom_gaji_bp = Blueprint('kom_gaji_bp', __name__, url_prefix='/api/kom-gaji')
kom_gaji_api = Api(kom_gaji_bp)

class KomponenGajiController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def post(self):
        json = request.get_json()

        schema = KomponenGajiReq()

        validated = schema.load(json)

        response = KomponenGajiService.create_kom_gaji(validated)

        return marshal(response, kom_gaji_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        result = KomponenGajiService.get_kom_gaji_pagination(validated)

        response = {
            'pages': result.pages,
            'total': result.total,
            'items': result.items,
        }

        return marshal(response, kom_gaji_pagination_fields), 200

class KomponenGajiByIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, kom_gaji_id):
        response = KomponenGajiService.get_kom_gaji_by_id(kom_gaji_id)

        return marshal(response, kom_gaji_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self, kom_gaji_id):
        json = request.get_json()

        schema = KomponenGajiReq()

        validated = schema.load(json)

        response = KomponenGajiService.update_kom_gaji(kom_gaji_id, validated)

        return marshal(response, kom_gaji_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def delete(self, kom_gaji_id):

        KomponenGajiService.delete_kom_gaji(kom_gaji_id)

        return None, 200

class AllKomponenGajiController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        response = KomponenGajiService.get_all_kom_gaji()

        return marshal(response, simple_kom_gaji_fields), 200


kom_gaji_api.add_resource(KomponenGajiController, '')
kom_gaji_api.add_resource(KomponenGajiByIdController, '/<string:kom_gaji_id>')
kom_gaji_api.add_resource(AllKomponenGajiController, '/all')