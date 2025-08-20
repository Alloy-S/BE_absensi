from app.repositories.dashboard_admin_repository import DashboardAdminRepository
from app.repositories.user_repository import UserRepository
from app.repositories.dashboard_user_repository import DashboardUserRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam

class DashboardAdminService:

    @staticmethod
    def get_dashboard_admin():

        result = DashboardAdminRepository.get_today_attendance_summary()

        response = {
            'hadir': 0,
            'terlambat': 0,
            'pulang_cepat': 0,
            'terlambat_pulang_cepat': 0,
            'izin': 0,
            'alpha': 0,
        }

        for row in result:
            status = row['final_status']
            jumlah = row['jumlah']

            status_key = status.lower().replace(' ', '_').replace(' & ', '_')

            if status_key in response:
                response[status_key] = jumlah

        return response


    @staticmethod
    def get_dashboard_total_active_users():
        result = DashboardAdminRepository.get_total_active_user()

        return {
            'total_active_users': result,
        }