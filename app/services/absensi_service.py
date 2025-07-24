from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.repositories.user_repository import UserRepository
from app.repositories.absensi_repository import AbsensiRepository
from datetime import datetime

from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode


class AbsensiService:
    @staticmethod
    def get_attendance_history(username, data):
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        search_filter = data.get('search')

        if not search_filter:
            now = datetime.now()
            search_filter = now.strftime('%Y-%m')

        return AbsensiRepository.get_absensi_history_by_month_year(
            user.id,
            data['page'],
            data['size'],
            search_filter
        )

    @staticmethod
    def get_attendance_history_detail_by_absensi_id(username, absensi_id):
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        data = AbsensiRepository.get_absensi_history_detail_by_absensi_id(user.id, absensi_id)

        if not data:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.ABSENSI_RESOURCE.value})

        return data

    @staticmethod
    def get_attendance_history_detail_by_date(username, date):
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        attendance_date = datetime.strptime(date, AppConstants.DATE_FORMAT.value).date()
        data = AbsensiRepository.get_absensi_history_detail_by_date(user.id, attendance_date)

        if not data:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.ABSENSI_RESOURCE.value})

        return data