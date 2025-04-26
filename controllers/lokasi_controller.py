from flask_restful import Resource, marshal_with, abort
from services.lokasi_service import LokasiService
from models.lokasi.lokasi_model import lokasi_fields, lokasi_args

class LokasiListController(Resource):
    # method_decorators = [jwt_required()]
    
    @marshal_with(lokasi_fields)
    def get(self):
        return LokasiService.get_all_lokasi();
    
    @marshal_with(lokasi_fields)
    def post(self):
        args = lokasi_args.parse_args()
        lokasi = LokasiService.create_lokasi(args["name"], args["latitude"], args["longitude"], args["toleransi"])
        
        if not lokasi:
            return abort(400, message="Lokasi tidak dapat dibuat")
        return lokasi, 201
    
class LokasiController(Resource):
    # method_decorators = [jwt_required()]
    
    @marshal_with(lokasi_fields)
    def get(self, id):
        lokasi = LokasiService.get_lokasi_by_id(id)
        if not lokasi:
            return  abort(404, message="Lokasi not found")
        return lokasi
    
    @marshal_with(lokasi_fields)
    def put(self, id):
        args=lokasi_args.parse_args()
        lokasi = LokasiService.update_lokasi(id, args["name"], args["latitude"], args["longitude"], args["toleransi"])
        if not lokasi:
            return  abort(404, message="Lokasi not found")
        return lokasi
    
    def delete(self, id):
        success = LokasiService.delete_lokasi(id)
        if not success:
            abort(404, message="Lokasi not found")
        return None, 200
    
   