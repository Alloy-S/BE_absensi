from datetime import datetime
from app.database import db
from app.entity import ApprovalIzin
from app.repositories.jatah_cuti_repository import JatahCutiRepository
from app.repositories.user_repository import UserRepository
from app.repositories.izin_repository import IzinRepository
from app.repositories.approval_izin_repository import ApprovalIzinRepository
from app.repositories.jenis_izin_repository import JenisIzinRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.utils.global_utils import format_string


class IzinService:

    @staticmethod
    def create_izin(username: str, data: dict):
        try:
            user = UserRepository.get_user_by_username(username)
            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            if not user.data_karyawan.pic:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.PIC_KARYAWAN.value})

            approver = user.data_karyawan.pic

            existing_izin = IzinRepository.get_izin_by_date(user.id, data['tgl_izin_start'])

            if existing_izin:
                raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE,
                                                params={'resource': AppConstants.IZIN_RESOURCE.value})

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
        return ApprovalIzinRepository.get_list_pagination(user.id, data.get('filter_month'), data.get('filter_status'),
                                                          data.get("page"), data.get("size"))

    @staticmethod
    def get_list_izin_approval_user(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalIzinRepository.get_list_pagination_approval_user(user.id, request.get("page"),
                                                                           request.get("size"),
                                                                           request.get("filter_month"),
                                                                           request.get("filter_status"))

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

    @staticmethod
    def approve_izin(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalIzinRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.IZIN_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.APPROVED.value
            approval.izin.status = AppConstants.APPROVED.value

            izin = approval.izin
            jenis_izin = izin.jenis_izin

            if jenis_izin.kuota_default > 0:
                start_date = izin.tgl_izin_start
                end_date = izin.tgl_izin_end

                durasi = (end_date - start_date).days + 1

                kuota_user = JatahCutiRepository.find_by_user_and_type(approval.user.id, jenis_izin.id, start_date.year)

                if kuota_user and kuota_user.sisa_kuota >= durasi:
                    kuota_user.kuota_terpakai += durasi
                    kuota_user.sisa_kuota -= durasi
                else:
                    raise GeneralException(ErrorCode.INSUFFICIENT_KUOTA_CUTI)

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.APPROVE_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.IZIN_RESOURCE.value}),
                                                         format_string(AppConstants.APPROVE_BODY.value, params={
                                                             'resource': AppConstants.IZIN_RESOURCE.value,
                                                             'nama_pengaju': approval.approval_user.fullname
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def reject_izin(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalIzinRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.APPROVAL_IZIN_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.REJECTED.value
            approval.izin.status = AppConstants.REJECTED.value

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.REJECT_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.APPROVAL_IZIN_RESOURCE.value}),
                                                         format_string(AppConstants.REJECT_BODY.value, params={
                                                             'resource': AppConstants.APPROVAL_IZIN_RESOURCE.value
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_detail_izin_by_approval_user(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalIzinRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_IZIN_RESOURCE.value})
        return result

    @staticmethod
    def get_izin_history_admin(data):

        return IzinRepository.get_history_izin_admin(
            data.get('page'),
            data.get('size'),
            data.get('filter_month'),
            data.get('search')
        )

    @staticmethod
    def get_izin_history_by_id(izin_id):
        return IzinRepository.get_izin_by_id(izin_id)
