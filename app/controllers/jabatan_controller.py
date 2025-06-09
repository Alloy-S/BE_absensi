from flask import Blueprint, request
from flask_restful import Api, Resource, marshal_with

from app.models.pagination_model import PaginationReq
from app.services.jabatan_service import JabatanService
from marshmallow import ValidationError
from app.models.jabatan.jabatan_req_model import JabatanReq
from app.models.jabatan.jabatan_res_model import jabatan_fields, jabatan_field, jabatan_pagination_fields

jabatan_bp = Blueprint('jabatan_bp', __name__, url_prefix='/api/jabatan')
jabatan_api = Api(jabatan_bp)

class JabatanListResource(Resource):
    @marshal_with(jabatan_pagination_fields)
    def get(self):
        print("Fetching all jabatan")
        
        queryparams = request.args

        schema = PaginationReq()

        try:
            validated = schema.load(queryparams)

            print(f"Fetching all Jabatan page={validated['page']}, per_page={validated['size']}")

            data = JabatanService.get_all_pagination(validated['page'], validated['size'], validated['search'])

            response = {
                "pages": data.pages,
                "total": data.total,
                "items": data.items
            }
            return response, 200
        except ValidationError as e:
            return {"message": e.messages}, 400


    
    def post(self):
        print("Creating jabatan")

        json_data = request.get_json()

        schema = JabatanReq()

        try:
            validated = schema.load(json_data)

            jabatan = JabatanService.create(validated["nama"], validated["parent_id"])

            if not jabatan:
                return {"message": "Jabatan Sudah Terdaftar"}, 400

            return None, 201
        except ValidationError as e:
            return {"message": e.messages}, 400
    

class JabatanAllResource(Resource):
    @marshal_with(jabatan_fields)
    def get(self):
        print("Fetching all jabatan without pagination")

        data = JabatanService.get_all()
        
        response = {
            "items": data
        }  
        
        return response, 200
    
class JabatanResource(Resource):
    @marshal_with(jabatan_field)
    def get(self, id):
        print(f"Fetching Jabatan by id: {id}")
        
        jabatan = JabatanService.get_by_id(id)
        
        if not jabatan:
            return {"message": "Jabatan tidak ditemukan"}, 404
        
        return jabatan, 200
    
    @marshal_with(jabatan_field)
    def put(self, id):
        print(f"Edit Jabatan: {id}")
        json_data = request.get_json()

        schema = JabatanReq()

        try:
            validated = schema.load(json_data)

            jabatan = JabatanService.update(id, validated["nama"], validated["parent_id"])

            if not jabatan:
                return {"message": "Gagal Melakukan Update jabatan"}, 400

            return jabatan, 200
        except ValidationError as e:
            return {"message": e.messages}, 400
    
    
    def delete(self, id):
        print(f"Delete Jabatan: {id}")
        jabatan = JabatanService.delete(id)
        
        if jabatan is False:
            return {"message": "Gagal Melakukan Delete jabatan"}, 400
        
        return None, 200

jabatan_api.add_resource(JabatanAllResource, '/all')
jabatan_api.add_resource(JabatanListResource, '')
jabatan_api.add_resource(JabatanResource, '/<string:id>')
