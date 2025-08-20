from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.models.dashboard.dashboard_admin_res import today_attendance_field, total_users_field
from app.services.dashboard_admin_service import DashboardAdminService
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request

dashboard_admin_bp = Blueprint('dashboard_admin_bp', __name__, url_prefix='/api/dashboard/admin')
dashboard_admin_api = Api(dashboard_admin_bp)


class DashboardAdminTodayAttedanceSummaryController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        response = DashboardAdminService.get_dashboard_admin()

        return marshal(response, today_attendance_field), 200

class DashboardAdminTotalUsersController(Resource):
    @role_required(AppConstants.ADMIN_GROUP.value)
    def get(self):
        response = DashboardAdminService.get_dashboard_total_active_users()

        return marshal(response, total_users_field), 200

dashboard_admin_api.add_resource(DashboardAdminTodayAttedanceSummaryController, '/attendance-summary')
dashboard_admin_api.add_resource(DashboardAdminTotalUsersController, '/total-users')
