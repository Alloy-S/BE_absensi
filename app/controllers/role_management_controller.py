from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required, permission_required
from app.models.role_management.role_management_req import UpdateRolesSchema
from app.services.role_management_service import RoleManagementService
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.models.role_management.role_management_res import user_roles_field, roles_field


role_management_bp = Blueprint('role_management_bp', __name__, url_prefix='/api/role-management')
role_management_api = Api(role_management_bp)

class RoleUserRoleByUserIdController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("role_management")
    def get(self, user_id):

        response = RoleManagementService.get_user_role_by_user_id(user_id)

        return marshal(response, user_roles_field), 200

    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("role_management")
    def put(self, user_id):
        json_data = request.get_json()
        schema = UpdateRolesSchema()

        validated = schema.load(json_data)

        RoleManagementService.update_user_role(user_id, validated)

        return None, 200


class RolesController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    @permission_required("role_management")
    def get(self):
        response = RoleManagementService.get_all_roles()

        return marshal(response, roles_field), 200

role_management_api.add_resource(RoleUserRoleByUserIdController, '/<string:user_id>')
role_management_api.add_resource(RolesController, '/roles')