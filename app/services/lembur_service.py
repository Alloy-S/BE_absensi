from datetime import datetime
from app.database import db
from app.repositories.user_repository import UserRepository
from app.repositories.lembur_repository import LemburRepository
from app.repositories.approval_lembur_repository import ApprovalLemburRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode


class LemburService:

    @staticmethod
    def create_lembur(username: str, data: dict):
        try:
            user = UserRepository.get_user_by_username(username)
            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approver = user.data_karyawan.pic

            lembur_payload = {
                'date_start': data['date_start'],
                'date_end': data['date_end'],
                'keterangan': data.get('keterangan', ''),
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'user_id': user.id
            }
            new_lembur = LemburRepository.create_lembur(lembur_payload)

            approval_payload = {
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'approval_user_id': approver.id,
                'user_id': user.id,
                'lembur_id': new_lembur.id
            }
            approval = ApprovalLemburRepository.create_approval_lembur(approval_payload)

            db.session.commit()

            return approval

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_list_lembur(username, data):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalLemburRepository.get_list_pagination(user.id,data.get('filter_month'),  data.get('filter_status'), data.get('page'), data.get('size'))

    @staticmethod
    def get_detail_approval_lembur(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalLemburRepository.get_detail_by_id(user.id, approval_id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.ABSENSI_RESOURCE.value})
        return result

    @staticmethod
    def cancel_approval_lembur(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        lembur_to_cancel = ApprovalLemburRepository.get_detail_by_id(user.id, approval_id)

        if not lembur_to_cancel:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.LEMBUR_RESOURCE.value})

        if lembur_to_cancel.status != AppConstants.WAITING_FOR_APPROVAL.value:
            raise GeneralException(ErrorCode.CANCELLATION_NOT_ALLOWED)

        try:
            ApprovalLemburRepository.delete_approval_lembur(lembur_to_cancel)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e