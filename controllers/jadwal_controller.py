from flask_restful import Resource, reqparse, fields, marshal_with, abort
from services.jadwal_kerja_service import JadwalKerjaService
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.jadwal_kerja_model import jadwal_args, jadwal_fields

class JadwalListController(Resource):
    # method_decorators = [jwt_required()]
    
    @marshal_with(jadwal_fields)
    def get(self):
        return JadwalKerjaService.get_all();
    
    @marshal_with(jadwal_fields)
    def post(self):
        args = jadwal_args.parse_args()
        
        jadwal = JadwalKerjaService.create(args["shift"], args["time_in"], args["time_out"], args["toler_in"], args['toler_out'])
       
        if not jadwal:
            return abort(400, message="Jadwal tidak dapat dibuat")
        return jadwal, 201
    
class JadwalController(Resource):
    # method_decorators = [jwt_required()]
    
    @marshal_with(jadwal_fields)
    def get(self, id):
        jadwal = JadwalKerjaService.get_by_id(id)
        if not jadwal:
            return  abort(404, message="Jadwal not found")
        return jadwal
    
    @marshal_with(jadwal_fields)
    def put(self, id):
        args=jadwal_args.parse_args()
        jadwal = JadwalKerjaService.update(id, args["shift"], args["time_in"], args["time_out"], args["toler_in"], args['time_out'])
        if not jadwal:
            return  abort(404, message="Jadwal not found")
        return jadwal
    
    def delete(self, id):
        success = JadwalKerjaService.delete(id)
        if not success:
            abort(404, message="Jadwal not found")
        return None, 200
    
   