from flask_restful import Resource, abort, Api, marshal

from app.filter.jwt_filter import role_required, permission_required
from app.models.pagination_model import PaginationReq
from app.services.jenis_izin_service import JenisIzinService
from flask import Blueprint, request
from app.utils.app_constans import AppConstants
from app.models.jenis_izin.jenis_izin_res import jenis_izin_fields, pagination_fields, jenis_izin_all_fields
from app.models.jenis_izin.jenis_izin_req import JenisIzinRequestSchema, PaginationReqSchema

jenis_izin_bp = Blueprint('jenis_izin_bp', __name__, url_prefix='/api/jenis-izin')
jenis_izin_api = Api(jenis_izin_bp)


class JenisIzinListController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_jenis_izin")
    def get(self):
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 10, type=int)
        search = request.args.get('search', None)

        result = JenisIzinService.get_jenis_izin_pagination(page=page, size=size, search=search)

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields)

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_jenis_izin")
    def post(self):
        json_data = request.get_json()
        schema = JenisIzinRequestSchema()

        validated_data = schema.load(json_data)

        response = JenisIzinService.create_jenis_izin(validated_data)
        return marshal(response, jenis_izin_fields), 201


class JenisIzinDetailController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_jenis_izin")
    def get(self, jenis_izin_id):
        response = JenisIzinService.get_jenis_izin_by_id(jenis_izin_id)
        return marshal(response, jenis_izin_fields)

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_jenis_izin")
    def put(self, jenis_izin_id):
        json_data = request.get_json()
        schema = JenisIzinRequestSchema()

        validated_data = schema.load(json_data)

        response = JenisIzinService.update_jenis_izin(jenis_izin_id, validated_data)
        return marshal(response, jenis_izin_fields)

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_jenis_izin")
    def delete(self, jenis_izin_id):
        JenisIzinService.delete_jenis_izin(jenis_izin_id)
        return None, 200

class JenisIzinAllController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        result = JenisIzinService.get_jenis_izin_all()

        response = {
            "items": result
        }
        return marshal(response, jenis_izin_all_fields), 200


jenis_izin_api.add_resource(JenisIzinListController, '')
jenis_izin_api.add_resource(JenisIzinDetailController, '/<string:jenis_izin_id>')
jenis_izin_api.add_resource(JenisIzinAllController, '/all')

