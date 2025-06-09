from flask_restful import Resource, marshal, abort, Api
from filter.jwt_filter import role_required
from models.pagination_model import PaginationReq
from services.lokasi_service import LokasiService
from models.lokasi.lokasi_req_model import LokasiReq
from models.lokasi.lokasi_res_model import lokasi_fields, pagination_fields, lokasi_field
from flask import request, Blueprint, jsonify
from marshmallow import ValidationError
from utils.app_constans import AppConstants

lokasi_bp = Blueprint('lokasi_bp', __name__, url_prefix='/api/lokasi')
lokasi_api = Api(lokasi_bp)

class LokasiListController(Resource):

    # @role_required(AppConstants.adminRole, AppConstants.hrdRole)
    def get(self):

        params = request.args

        schema = PaginationReq()

        try:
            validated = schema.load(params)

            result = LokasiService.get_all_lokasi_pagination(page=validated['page'], size=validated['size'], search=validated['search'])

            response = {
                "pages": result.pages,
                "total": result.total,
                "items": result.items
            }

            return marshal(response, pagination_fields), 200

        except ValidationError as e:
            return {'message': e.messages}, 400
        except Exception as _:
            return {'message': 'Internal Server Error'}, 500

    def post(self):
        json = request.get_json()

        print(json)
        schema = LokasiReq()

        try:
            validated = schema.load(json)

            lokasi = LokasiService.create_lokasi(validated["name"], validated["latitude"], validated["longitude"], validated["toleransi"])

            if not lokasi:
                return abort(400, message="Lokasi tidak dapat dibuat")

            return None, 201
        except ValidationError as e:
            return {'message': e.messages}, 400
    
class LokasiController(Resource):

    def get(self, id):
        lokasi = LokasiService.get_lokasi_by_id(id)
        if not lokasi:
            return  abort(404, message="Lokasi not found")
        return marshal(lokasi, lokasi_field), 200

    def put(self, id):
        json = request.get_json()

        schema = LokasiReq()

        try:
            validated = schema.load(json)

            lokasi = LokasiService.update_lokasi(id, validated["name"], validated["latitude"], validated["longitude"], validated["toleransi"])

            if not lokasi:
                return  abort(404, message="Lokasi not found")

            return marshal(lokasi, lokasi_fields), 200
        except ValidationError as e:
            return {'message': str(e)}, 400

    
    def delete(self, id):
        success = LokasiService.delete_lokasi(id)
        if not success:
            abort(404, message="Lokasi not found")
        return None, 200

class LokasiAllController(Resource):

    def get(self):

        result = LokasiService.get_all_lokasi()
        res = {
            "items": result
        }
        return marshal(res, lokasi_fields), 200

lokasi_api.add_resource(LokasiAllController, '/all')
lokasi_api.add_resource(LokasiListController, '')
lokasi_api.add_resource(LokasiController, '/<string:id>')
    
   