from flask_restful import Resource, abort, Api, marshal

from app.filter.jwt_filter import role_required
from app.models.pagination_model import PaginationReq
from app.models.users.users_req_model import UserSchema
from app.services.jatah_cuti_service import JatahCutiService
from flask import Blueprint, request
from app.utils.app_constans import AppConstants
from app.models.kuota_cuti.kuota_cuti_req import JatahCutiUpdateRequestSchema, JatahCutiCreateRequestSchema
from app.models.kuota_cuti.kuota_cuti_res import jatah_cuti_fields, pagination_fields, jenis_izin_simple_fields
from datetime import datetime

jatah_cuti_bp = Blueprint('jatah_cuti_bp', __name__, url_prefix='/api/kuota-cuti')
jatah_cuti_api = Api(jatah_cuti_bp)

class JatahCutiListController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, user_id):
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)

        response = JatahCutiService.get_list_for_user(user_id, page, size)

        return marshal(response, pagination_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def post(self, user_id):
        json = request.get_json()

        schema = JatahCutiCreateRequestSchema()

        validated = schema.load(json)

        response = JatahCutiService.create_jatah_cuti(user_id, validated)

        return marshal(response, jatah_cuti_fields), 201

class JatahCutiDetailController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, jatah_cuti_id):

        jatah_cuti = JatahCutiService.get_detail(jatah_cuti_id)
        return marshal(jatah_cuti, jatah_cuti_fields), 200


    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self, jatah_cuti_id):
        json_data = request.get_json()
        schema = JatahCutiUpdateRequestSchema()

        validated_data = schema.load(json_data)


        updated_jatah_cuti = JatahCutiService.adjust_kuota(jatah_cuti_id, validated_data)
        return marshal(updated_jatah_cuti, jatah_cuti_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def delete(self, jatah_cuti_id):
        JatahCutiService.delete_jatah_cuti(jatah_cuti_id)
        return None, 200


class JatahCutiGenerateController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def post(self):

        target_year = datetime.now().year

        response = JatahCutiService.generate_kuota_tahunan(target_year)

        return response, 200

jatah_cuti_api.add_resource(JatahCutiListController, '/user/<string:user_id>')
jatah_cuti_api.add_resource(JatahCutiDetailController, '/<string:jatah_cuti_id>')
jatah_cuti_api.add_resource(JatahCutiGenerateController, '/generate/tahunan')