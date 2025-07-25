from flask_restful import Resource, abort, Api, marshal

from app.models.jadwalKerja import jadwal_kerja_req_model
from app.models.pagination_model import PaginationReq
from app.services.jadwal_kerja_service import JadwalKerjaService
from app.models.jadwalKerja.jadwal_kerja_req_model import JadwalKerjaRequestSchema
from app.models.jadwalKerja.jadwal_kerja_res_model import jadwal_kerja_field, jadwal_pagination_fields, jadwal_fields
from flask import Blueprint, request
from marshmallow import ValidationError

jadwal_bp = Blueprint('jadwal_bp', __name__, url_prefix='/api/jadwal')
jadwal_api = Api(jadwal_bp)

class JadwalFetchAllController(Resource):

    def get(self):
        results = JadwalKerjaService.get_all()

        res = {
            "items": results
        }
        return marshal(res, jadwal_fields), 200

class JadwalListController(Resource):

    

    def get(self):
        params = request.args

        schema = PaginationReq()

        try:
            validated = schema.load(params)

            results = JadwalKerjaService.get_all_pagination(page=validated["page"], size=validated["size"], search=validated["search"])

            res = {
                "pages": results.pages,
                "total": results.total,
                "items": results.items
            }
            return marshal(res, jadwal_pagination_fields), 200

        except ValidationError as e:
            return abort(400, message=e.messages)

    def post(self):
        json = request.get_json()

        schema = JadwalKerjaRequestSchema()

        try:
            validated = schema.load(json)
        
            jadwal = JadwalKerjaService.create(kode=validated["kode"], shift=validated["shift"], details=validated["detail_jadwal_kerja"])

            if not jadwal:
                return abort(400, message="Jadwal tidak dapat dibuat")

            return None, 201
        except ValidationError as e:
            return abort(400, message=e.messages)
    
class JadwalController(Resource):

    def get(self, jadwal_id):
        response = JadwalKerjaService.get_by_id(jadwal_id)


        return marshal(response, jadwal_kerja_field), 200
    

    def put(self, jadwal_id):
        json = request.get_json()

        schema = JadwalKerjaRequestSchema()

        try:
            validated = schema.load(json)
            jadwal = JadwalKerjaService.update(jadwal_id, kode=validated["kode"], shift=validated["shift"], details=validated["detail_jadwal_kerja"])
            if not jadwal:
                return  abort(404, message="Jadwal not found")
            return marshal(jadwal, jadwal_kerja_field), 200
        except ValidationError as e:
            return abort(400, message=e.messages)
    
    def delete(self, jadwal_id):
        success = JadwalKerjaService.delete(jadwal_id)
        if not success:
            abort(404, message="Jadwal not found")
        return None, 200
    
jadwal_api.add_resource(JadwalFetchAllController, '/all')
jadwal_api.add_resource(JadwalListController, '')
jadwal_api.add_resource(JadwalController, '/<string:jadwal_id>')