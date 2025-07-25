from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.approval_koreksi_repository import ApprovalKoreksiRepository
from app.repositories.absensi_repository import AbsensiRepository
from app.repositories.user_repository import UserRepository
from app.repositories.detail_approval_koreksi_repository import DetailApprovalKoreksiRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db
from datetime import datetime


class KoreksiKehadiranService:

    @staticmethod
    def get_list_koreksi(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalKoreksiRepository.get_list_pagination(user.id, request.get("page"),  request.get("size"), request.get("filter_month"), request.get("filter_status"))

    @staticmethod
    def get_detail_koreksi(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalKoreksiRepository.get_detail_by_id(user.id, approval_id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.ABSENSI_RESOURCE.value})
        return result

    @staticmethod
    def create_koreksi_kehadiran(username, data):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            attendance_date = data['date']
            absensi_id = data.get('absensi_id')

            existing_approval = ApprovalKoreksiRepository.find_by_user_and_date(user.id, attendance_date)
            if existing_approval:
                ApprovalKoreksiRepository.delete_koreksi(existing_approval)

            approval = ApprovalKoreksiRepository.create_approval_koreksi_user({
                'absensi_date': data['date'],
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'approval_user_id': user.data_karyawan.pic.id,
                'user_id': user.id,
                'absensi_id': absensi_id,
                'catatan_pengajuan': data.get('catatan_pengajuan', '')
            })

            DetailApprovalKoreksiRepository.create_detaill_approval_koreksi_user({
                'approval_koreksi_id': approval.id,
                'requested_datetime': data['time_in'],
                'type': AppConstants.ATTENDANCE_IN.value,
            })

            DetailApprovalKoreksiRepository.create_detaill_approval_koreksi_user({
                'approval_koreksi_id': approval.id,
                'requested_datetime': data['time_out'],
                'type': AppConstants.ATTENDANCE_OUT.value,
            })

            db.session.commit()
            return approval
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def cancel_koreksi(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        koreksi_to_cancel = ApprovalKoreksiRepository.get_detail_by_id(user.id, approval_id)

        if not koreksi_to_cancel:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_KOREKSI_RESOURCE.value})

        if koreksi_to_cancel.status != AppConstants.WAITING_FOR_APPROVAL.value:
            raise GeneralException(ErrorCode.CANCELLATION_NOT_ALLOWED)

        try:
            ApprovalKoreksiRepository.delete_koreksi(koreksi_to_cancel)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
