from flask import Blueprint, request
from flask_restful import Api, Resource, marshal_with, marshal
from app.filter.jwt_filter import role_required
from app.models.pagination_model import PaginationReq
from app.services.jabatan_service import JabatanService
from marshmallow import ValidationError
from app.models.jabatan.jabatan_req_model import JabatanReq
from app.models.jabatan.jabatan_res_model import jabatan_fields, jabatan_field, jabatan_pagination_fields
from app.utils.app_constans import AppConstants

jabatan_bp = Blueprint('jabatan_bp', __name__, url_prefix='/api/jabatan')
jabatan_api = Api(jabatan_bp)

class JabatanListResource(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        
        queryparams = request.args

        schema = PaginationReq()

        validated = schema.load(queryparams)

        data = JabatanService.get_all_pagination(validated['page'], validated['size'], validated['search'])

        response = {
            "pages": data.pages,
            "total": data.total,
            "items": data.items
        }
        return marshal(response, jabatan_pagination_fields), 200


    @role_required(AppConstants.ADMIN_GROUP.value)
    def post(self):

        json_data = request.get_json()

        schema = JabatanReq()

        validated = schema.load(json_data)

        jabatan = JabatanService.create(validated["nama"], validated["parent_id"])

        return marshal(jabatan, jabatan_field), 201

    

class JabatanAllResource(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        print("Fetching all jabatan without pagination")

        data = JabatanService.get_all()
        
        response = {
            "items": data
        }  
        
        return marshal(response, jabatan_fields), 200
    
class JabatanResource(Resource):

    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self, id):
        
        jabatan = JabatanService.get_by_id(id)
        
        return marshal(jabatan, jabatan_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def put(self, id):

        json_data = request.get_json()

        schema = JabatanReq()

        validated = schema.load(json_data)

        jabatan = JabatanService.update(id, validated["nama"], validated["parent_id"])

        return marshal(jabatan, jabatan_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    def delete(self, id):
        jabatan = JabatanService.delete(id)
        
        return None, 200

jabatan_api.add_resource(JabatanAllResource, '/all')
jabatan_api.add_resource(JabatanListResource, '')
jabatan_api.add_resource(JabatanResource, '/<string:id>')
