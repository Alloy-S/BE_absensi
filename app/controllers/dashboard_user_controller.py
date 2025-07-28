from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.pagination_model import PaginationReq
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.dashboard_user_service import DashboardUserService
from app.models.dashboard.dashbaord_user_res import approval_fields

dashboard_user_bp = Blueprint('dashboard_user_bp', __name__, url_prefix='/api/dashboard/user')
dashboard_user_api = Api(dashboard_user_bp)

class DashboardUserController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        username = get_jwt_identity()

        response = DashboardUserService.get_waiting_for_approvals_user(username)

        return marshal(response, approval_fields), 200

dashboard_user_api.add_resource(DashboardUserController, '/approvals')