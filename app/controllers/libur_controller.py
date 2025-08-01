from app.services.libur_service import LiburService
from flask import request, Blueprint
from flask_restful import Resource, Api, marshal
from app.models.pagination_model import PaginationReq
from app.models.libur.libur_req import LiburRequestSchema
from app.models.libur.libur_res import libur_pagination_fields, libur_field
from app.filter.jwt_filter import role_required, permission_required
from app.utils.app_constans import AppConstants

libur_bp = Blueprint('libur_bp', __name__, url_prefix='/api/libur')
libur_api = Api(libur_bp)

class LiburPaginationController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_libur")
    def get(self):
        params = request.args

        schema = PaginationReq()

        validated = schema.load(params)

        result = LiburService.get_libur_pagination(page=validated['page'], size=validated['size'], search=validated['search'])

        response = {
            "pages": result.pages,
            "total": result.total,
            "items": result.items
        }

        return marshal(response, libur_pagination_fields), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_libur")
    def post(self):
        params = request.json
        schema = LiburRequestSchema()

        validated = schema.load(params)

        response = LiburService.create_libur(validated)

        return marshal(response, libur_field), 201


class LiburController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_libur")
    def get(self, libur_id):
        response = LiburService.get_libur_by_id(libur_id)

        return marshal(response, libur_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_libur")
    def put(self, libur_id):
        data = request.get_json()

        schema = LiburRequestSchema()

        validated = schema.load(data)

        response = LiburService.update_libur(libur_id, validated)

        return marshal(response, libur_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("config_libur")
    def delete(self, libur_id):
        response = LiburService.delete_libur(libur_id)
        return response, 200


libur_api.add_resource(LiburPaginationController, '')
libur_api.add_resource(LiburController, '/<string:libur_id>')
