from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.repositories.approval_koreksi_repository import ApprovalKoreksiRepository
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
        absensi_data = AbsensiRepository.get_absensi_history_detail_by_date(user.id, attendance_date)
        if absensi_data:
            return AbsensiService.map_absensi_response(absensi_data)

        existing_approval = ApprovalKoreksiRepository.find_by_user_and_date(user.id, attendance_date)
        if existing_approval:
            return AbsensiService.map_approval_response(existing_approval)

        raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,params={'resource': AppConstants.ABSENSI_BY_DATE_RESOURCE.value})

    @staticmethod
    def map_absensi_response(absensi):
        if not absensi:
            return None

        detail_in = next((d for d in absensi.detail_absensi if d.type == 'IN'), None)
        detail_out = next((d for d in absensi.detail_absensi if d.type == 'OUT'), None)

        return {
            "date": absensi.date.isoformat(),
            "absensi_id": absensi.id,
            "time_in": detail_in.date.isoformat() if detail_in else None,
            "time_out": detail_out.date.isoformat() if detail_out else None
        }

    @staticmethod
    def map_approval_response(approval):
        if not approval:
            return None

        detail_in = next((d for d in approval.detail_approval if d.type == 'IN'), None)
        detail_out = next((d for d in approval.detail_approval if d.type == 'OUT'), None)

        return {
            "date": approval.absensi_date.isoformat(),
            "absensi_id": None,
            "time_in": detail_in.requested_datetime.isoformat() if detail_in else None,
            "time_out": detail_out.requested_datetime.isoformat() if detail_out else None
        }

    @staticmethod
    def get_absensi_history_admin(data):

        return AbsensiRepository.get_history_absensi_admin(
            data.get('page'),
            data.get('size'),
            data.get('filter_month'),
            data.get('search')
        )

    @staticmethod
    def get_absensi_history_by_id(absensi_id):
        return AbsensiRepository.get_absensi_by_id(absensi_id)

