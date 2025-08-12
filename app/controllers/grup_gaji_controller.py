from flask_restful import Resource, abort, Api, marshal

from app.models.grup_gaji.grup_gaji_res import grup_gaji_fields, grup_gaji_pagination_fields, kode_perhitungan_fields, \
    grup_gaji_users_fields
from app.services.grup_gaji_service import GrupGajiService
from app.models.grup_gaji.grup_gaji_req import GrupGajiReq
from app.filter.jwt_filter import role_required, permission_required
from app.models.pagination_model import PaginationReq
from flask import Blueprint, request
from app.utils.app_constans import AppConstants

grup_gaji_bp = Blueprint('grup_gaji_bp', __name__, url_prefix='/api/grup-gaji')
grup_gaji_api = Api(grup_gaji_bp)

class GrupGajiController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def post(self):
        json = request.get_json()

        schema = GrupGajiReq()

        validated = schema.load(json)

        response = GrupGajiService.create_grup_gaji(validated)

        return marshal(response, grup_gaji_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        response = GrupGajiService.get_paginated_grup_gaji(validated)

        return marshal(response, grup_gaji_pagination_fields), 200

class GrupGajiByIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, grup_gaji_id):
        response = GrupGajiService.get_grup_gaji_by_id(grup_gaji_id)

        return marshal(response, grup_gaji_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self, grup_gaji_id):
        json = request.get_json()

        schema = GrupGajiReq()

        validated = schema.load(json)

        response = GrupGajiService.update_grup_gaji(grup_gaji_id, validated)

        return marshal(response, grup_gaji_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def delete(self, grup_gaji_id):

        response = GrupGajiService.delete_grup_gaji(grup_gaji_id)

        return response, 200

class KodePerhitunganController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        response = GrupGajiService.get_all_kode_perhitungan()

        return marshal(response, kode_perhitungan_fields), 200

class AllGrupGajiController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        response = GrupGajiService.get_all_grup_gaji()
        return marshal(response, grup_gaji_fields), 200

class GrupGajiUsersController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, grup_gaji_id):
        response = GrupGajiService.get_grup_gaji_users(grup_gaji_id)

        return marshal(response, grup_gaji_users_fields), 200

grup_gaji_api.add_resource(GrupGajiController, '')
grup_gaji_api.add_resource(GrupGajiByIdController, '/<string:grup_gaji_id>')
grup_gaji_api.add_resource(KodePerhitunganController, '/kode-perhitungan')
grup_gaji_api.add_resource(AllGrupGajiController, '/all')
grup_gaji_api.add_resource(GrupGajiUsersController, '/<string:grup_gaji_id>/users')