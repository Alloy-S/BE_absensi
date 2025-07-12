from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.perusahaan.perusahaan_req import PerusahaanSchema
from app.models.perusahaan.perusahaan_res import perusahaan_field
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.perusahaan_service import PerusahaanService

perusahaan_bp = Blueprint('perusahaan_bp', __name__, url_prefix='/api/perusahaan')
perusahaan_api = Api(perusahaan_bp)

class PerusahaanController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):

        response = PerusahaanService.get_profile_perusahaan()
        return marshal(response, perusahaan_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self):
        username = get_jwt_identity()
        json_data = request.get_json()
        schema = PerusahaanSchema()

        validated = schema.load(json_data)

        response = PerusahaanService.edit_profile_perusahaan(username, validated)

        return marshal(response, perusahaan_field), 200

perusahaan_api.add_resource(PerusahaanController, '')