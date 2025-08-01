from flask_restful import Resource, marshal, abort, Api

from app.utils.app_constans import AppConstants
from app.filter.jwt_filter import role_required, permission_required
from app.models.pagination_model import PaginationReq
from app.services.lokasi_service import LokasiService
from app.models.lokasi.lokasi_req_model import LokasiReq
from app.models.lokasi.lokasi_res_model import lokasi_fields, pagination_fields, lokasi_field
from flask import request, Blueprint

lokasi_bp = Blueprint('lokasi_bp', __name__, url_prefix='/api/lokasi')
lokasi_api = Api(lokasi_bp)

class LokasiListController(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_lokasi")
    def get(self):

        params = request.args

        schema = PaginationReq()


        validated = schema.load(params)

        result = LokasiService.get_all_lokasi_pagination(page=validated['page'], size=validated['size'], search=validated['search'])

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, pagination_fields), 200



    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_lokasi")
    def post(self):
        json = request.get_json()


        schema = LokasiReq()


        validated = schema.load(json)

        lokasi = LokasiService.create_lokasi(validated["name"], validated["latitude"], validated["longitude"], validated["toleransi"])

        return None, 201

    
class LokasiController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_lokasi")
    def get(self, id):
        lokasi = LokasiService.get_lokasi_by_id(id)

        return marshal(lokasi, lokasi_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_lokasi")
    def put(self, id):
        json = request.get_json()

        schema = LokasiReq()


        validated = schema.load(json)

        lokasi = LokasiService.update_lokasi(id, validated["name"], validated["latitude"], validated["longitude"], validated["toleransi"])

        return marshal(lokasi, lokasi_fields), 200


    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_lokasi")
    def delete(self, id):
        success = LokasiService.delete_lokasi(id)

        return None, 200

class LokasiAllController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_lokasi")
    def get(self):

        result = LokasiService.get_all_lokasi()
        res = {
            "items": result
        }
        return marshal(res, lokasi_fields), 200

lokasi_api.add_resource(LokasiAllController, '/all')
lokasi_api.add_resource(LokasiListController, '')
lokasi_api.add_resource(LokasiController, '/<string:id>')
    
   