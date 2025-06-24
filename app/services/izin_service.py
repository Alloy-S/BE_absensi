from datetime import datetime
from app.database import db
from app.repositories.user_repository import UserRepository
from app.repositories.izin_repository import IzinRepository
from app.repositories.approval_izin_repository import ApprovalIzinRepository
from app.repositories.jenis_izin_repository import JenisIzinRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode


class IzinService:

    @staticmethod
    def create_izin(username: str, data: dict):
        try:
            user = UserRepository.get_user_by_username(username)
            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approver = user.data_karyawan.pic

            izin_payload = {
                'tgl_izin_start': data['tgl_izin_start'],
                'tgl_izin_end': data['tgl_izin_end'],
                'keterangan': data.get('keterangan', ''),
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'jenis_izin_id': data['jenis_izin_id'],
                'user_id': user.id
            }
            new_izin = IzinRepository.create_izin(izin_payload)

            approval_payload = {
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'approval_user_id': approver.id,
                'user_id': user.id,
                'izin_id': new_izin.id
            }
            approval = ApprovalIzinRepository.create_approval_izin(approval_payload)

            db.session.commit()

            return approval

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_list_izin(username, data):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalIzinRepository.get_list_pagination(user.id, data['filter_status'], data['page'], data['size'])

    @staticmethod
    def get_detail_approval_izin(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalIzinRepository.get_detail_by_id(user.id, approval_id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.ABSENSI_RESOURCE.value})
        return result

    @staticmethod
    def cancel_approval_izin(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        izin_to_cancel = ApprovalIzinRepository.get_detail_by_id(user.id, approval_id)

        if not izin_to_cancel:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.IZIN_RESOURCE.value})

        if izin_to_cancel.status != AppConstants.WAITING_FOR_APPROVAL.value:
            raise GeneralException(ErrorCode.CANCELLATION_NOT_ALLOWED)

        try:
            ApprovalIzinRepository.delete_approval_izin(izin_to_cancel)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_jenis_izin():
        return JenisIzinRepository.get_all_jenis_izin()