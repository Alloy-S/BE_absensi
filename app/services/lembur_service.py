from datetime import datetime
from app.database import db
from app.repositories.user_repository import UserRepository
from app.repositories.lembur_repository import LemburRepository
from app.repositories.approval_lembur_repository import ApprovalLemburRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.utils.global_utils import format_string


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

    @staticmethod
    def get_list_lembur_approval_user(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalLemburRepository.get_list_pagination_approval_user(user.id, request.get("page"),
                                                                           request.get("size"),
                                                                           request.get("filter_month"),
                                                                           request.get("filter_status"))

    @staticmethod
    def get_detail_lembur_by_approval_user(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalLemburRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value})
        return result

    @staticmethod
    def approve_lembur(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalLemburRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.APPROVED.value
            approval.lembur.status = AppConstants.APPROVED.value

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.APPROVE_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value}),
                                                         format_string(AppConstants.APPROVE_BODY.value, params={
                                                             'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value,
                                                             'nama_pengaju': approval.approval_user.fullname
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def reject_lembur(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalLemburRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.REJECTED.value
            approval.lembur.status = AppConstants.REJECTED.value

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.REJECT_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value}),
                                                         format_string(AppConstants.REJECT_BODY.value, params={
                                                             'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value,
                                                             'nama_pengaju': approval.approval_user.fullname
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e