from flask_restful import Resource, abort, Api, marshal

from app.filter.jwt_filter import role_required
from app.models.pagination_model import PaginationReq
from app.services.jenis_izin_service import JenisIzinService
from flask import Blueprint, request
from app.utils.app_constans import AppConstants
from app.models.jenis_izin.jenis_izin_res import jenis_izin_fields, pagination_fields
from app.models.jenis_izin.jenis_izin_req import JenisIzinRequestSchema, PaginationReqSchema

jenis_izin_bp = Blueprint('jenis_izin_bp', __name__, url_prefix='/api/jenis-izin')
jenis_izin_api = Api(jenis_izin_bp)


class JenisIzinListController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
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
    def post(self):
        json_data = request.get_json()
        schema = JenisIzinRequestSchema()

        validated_data = schema.load(json_data)

        new_jenis_izin = JenisIzinService.create_jenis_izin(validated_data)
        return marshal(new_jenis_izin, jenis_izin_fields), 201


class JenisIzinDetailController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, jenis_izin_id):
        jenis_izin = JenisIzinService.get_jenis_izin_by_id(jenis_izin_id)
        return marshal(jenis_izin, jenis_izin_fields)

    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self, jenis_izin_id):
        json_data = request.get_json()
        schema = JenisIzinRequestSchema()

        validated_data = schema.load(json_data)

        updated_jenis_izin = JenisIzinService.update_jenis_izin(jenis_izin_id, validated_data)
        return marshal(updated_jenis_izin, jenis_izin_fields)

    @role_required(AppConstants.ADMIN_GROUP.value)
    def delete(self, jenis_izin_id):
        JenisIzinService.delete_jenis_izin(jenis_izin_id)
        return None, 200


jenis_izin_api.add_resource(JenisIzinListController, '')
jenis_izin_api.add_resource(JenisIzinDetailController, '/<string:jenis_izin_id>')
