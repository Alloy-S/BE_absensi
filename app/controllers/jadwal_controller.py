from flask_restful import Resource, marshal_with, abort, Api

from app.models.pagination_model import PaginationReq
from app.repositories.jadwal_kerja_repository import JadwalKerjaRepository
from app.services.jadwal_kerja_service import JadwalKerjaService
from app.models.jadwalKerja.jadwal_kerja_req_model import JadwalKerjaRequestSchema
from app.models.jadwalKerja.jadwal_kerja_res_model import jadwal_kerja_field, jadwal_pagination_fields, jadwal_fields
from flask import Blueprint, request
from marshmallow import ValidationError

jadwal_bp = Blueprint('jadwal_bp', __name__, url_prefix='/api/jadwal')
jadwal_api = Api(jadwal_bp)

class JadwalFetchAllController(Resource):
    @marshal_with(jadwal_fields)
    def get(self):
        results = JadwalKerjaRepository.get_all()

        res = {
            "items": results
        }
        return res, 200

class JadwalListController(Resource):
    # method_decorators = [jwt_required()]
    
    @marshal_with(jadwal_pagination_fields)
    def get(self):
        params = request.args

        schema = PaginationReq()

        try:
            validated = schema.load(params)

            results = JadwalKerjaRepository.get_all_pagination(page=validated["page"], size=validated["size"], search=validated["search"])

            res = {
                "pages": results.pages,
                "total": results.total,
                "items": results.items
            }
            return res, 200

        except ValidationError as e:
            return abort(400, message=e.messages)

    def post(self):
        json = request.get_json()

        schema = JadwalKerjaRequestSchema()

        try:
            validated = schema.load(json)
        
            jadwal = JadwalKerjaService.create(kode=validated["kode"], shift=validated["shift"], isSameHour=validated["is_same_hour"], details=validated["detail_jadwal_kerja"])

            if not jadwal:
                return abort(400, message="Jadwal tidak dapat dibuat")

            return None, 201
        except ValidationError as e:
            return abort(400, message=e.messages)
    
class JadwalController(Resource):
    # method_decorators = [jwt_required()]
    
    @marshal_with(jadwal_kerja_field)
    def get(self, id):
        jadwal = JadwalKerjaService.get_by_id(id)

        if not jadwal:
            return  abort(404, message="Jadwal not found")
        return jadwal
    
    @marshal_with(jadwal_kerja_field)
    def put(self, id):
        json = request.get_json()

        schema = JadwalKerjaRequestSchema()

        try:
            validated = schema.load(json)
            jadwal = JadwalKerjaService.update(id, kode=validated["kode"], shift=validated["shift"], isSameHour=validated["is_same_hour"], details=validated["detail_jadwal_kerja"])
            if not jadwal:
                return  abort(404, message="Jadwal not found")
            return jadwal
        except ValidationError as e:
            return abort(400, message=e.messages)
    
    def delete(self, id):
        success = JadwalKerjaService.delete(id)
        if not success:
            abort(404, message="Jadwal not found")
        return None, 200
    
jadwal_api.add_resource(JadwalFetchAllController, '/all')
jadwal_api.add_resource(JadwalListController, '')
jadwal_api.add_resource(JadwalController, '/<string:id>')