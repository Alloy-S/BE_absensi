from app.repositories.dashboard_admin_repository import DashboardAdminRepository
from app.repositories.detail_jadwal_kerja_repository import DetailJadwalKerjaRepository
from app.repositories.jadwal_kerja_repository import JadwalKerjaRepository
from app.repositories.libur_repository import LiburRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from datetime import datetime

class DashboardAdminService:

    @staticmethod
    def get_dashboard_admin():
        today = datetime.today()
        # today = '2025-08-26'
        result = DashboardAdminRepository.get_today_attendance_summary(today)

        response = {
            'libur': False,
            'hadir': 0,
            'datang_terlambat': 0,
            'pulang_cepat': 0,
            'datang_terlambat_pulang_cepat': 0,
            'izin': 0,
            'alpha': 0,
        }

        libur = LiburRepository.get_libur_by_date(today.date())
        if libur:
            response['libur'] = True
            return response

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

        response = {
            'user_bulanan': 0,
            'user_harian': 0,
        }

        for row in result:

            tipe = row['tipe_karyawan']
            jumlah = row['jumlah']

            if tipe == 'bulanan':
                response['user_bulanan'] = jumlah
            elif tipe == 'harian/borongan':
                response['user_harian'] = jumlah

        return response