from flask import Blueprint
from flask_restful import Api, Resource, marshal_with
from services.jabatan_service import JabatanService

from models.jabatan_model import jabatan_fields, pagination_args, jabatan_pagination_fields, jabatan_args, jabatan_field

jabatan_bp = Blueprint('jabatan_bp', __name__, url_prefix='/api/jabatan')
jabatan_api = Api(jabatan_bp)

class JabatanListResource(Resource):
    @marshal_with(jabatan_pagination_fields)
    def get(self):
        print("Fetching all jabatan")
        
        args = pagination_args.parse_args()
        
        print(f"Fetching all Jabatan page={args['page']}, per_page={args['size']}")
    
        data = JabatanService.get_all_pagination(args['page'], args['size'], args['search'])
        
        response = {
            "pages": data.pages,
            "total": data.total,
            "items": data.items
        }
        return response, 200
    
    def post(self):
        print("Creating jabatan")
        
        args = jabatan_args.parse_args()
        
        jabatan = JabatanService.create(args["nama"], args["parent_id"])
        
        if not jabatan:
            return {"message": "Jabatan Sudah Terdaftar"}, 400
        
        return None, 201
    

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
        args = jabatan_args.parse_args()
        jabatan = JabatanService.update(id, args["nama"], args["parent_id"])
        
        if not jabatan:
            return {"message": "Gagal Melakukan Update jabatan"}, 400
        
        return jabatan, 200
    
    
    def delete(self, id):
        print(f"Delete Jabatan: {id}")
        jabatan = JabatanService.delete(id)
        
        if jabatan is False:
            return {"message": "Gagal Melakukan Delete jabatan"}, 400
        
        return None, 200

jabatan_api.add_resource(JabatanAllResource, '/all')
jabatan_api.add_resource(JabatanListResource, '')
jabatan_api.add_resource(JabatanResource, '/<string:id>')
