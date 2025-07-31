from app.database import db
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.repositories.user_repository import UserRepository
from app.repositories.absensi_borongan_repository import AbsensiBoronganRepository
from app.repositories.detail_absensi_borongan_repository import DetailAbsensiBoronganRepository
from app.repositories.approval_absensi_borongan_repository import ApprovalAbsensiBoronganRepository
from app.repositories.harga_harian_borongan_repository import HargaHarianBoronganRepository
from app.utils.global_utils import format_string


class AbsensiBoronganService:
    @staticmethod
    def create_absensi_borongan(username, req_data):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approver = user.data_karyawan.pic
            if not approver:
                raise GeneralException(ErrorCode.APPROVER_NOT_FOUND)

            for detail_data in req_data['details']:
                harga = HargaHarianBoronganRepository.get_harga_by_id(detail_data['harga_id'])

                if not harga:
                    raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                    params={'resource': AppConstants.HARGA_RESOURCE.value})

                harga_normal = float(harga.harga_normal)
                harga_lembur = float(harga.harga_lembur)

                total = (detail_data['ton_normal'] * harga_normal) + (detail_data['ton_lembur'] * harga_lembur)

                detail_data['total'] = total

            total_keseluruhan = sum(detail['total'] for detail in req_data['details'])

            new_absensi = AbsensiBoronganRepository.create({
                "total": total_keseluruhan,
                "date": req_data['date'],
                "status": AppConstants.WAITING_FOR_APPROVAL.value,
            })

            for detail_data in req_data['details']:
                DetailAbsensiBoronganRepository.create(
                    ton_normal=detail_data['ton_normal'],
                    ton_lembur=detail_data['ton_lembur'],
                    tipe=detail_data['type'],
                    total=detail_data['total'],
                    user_id=detail_data['user_id'],
                    absensi_borongan_id=new_absensi.id,
                    harga_id=detail_data['harga_id']
                )

            new_approval = ApprovalAbsensiBoronganRepository.create(
                status=AppConstants.WAITING_FOR_APPROVAL.value,
                approval_user_id=approver.id,
                user_id=user.id,
                absensi_borongan_id=new_absensi.id
            )

            db.session.commit()
            return new_approval
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_list_absensi_borongan(username, data):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})
        return ApprovalAbsensiBoronganRepository.get_list_pagination(user.id, data.get('filter_month'),
                                                                     data.get('filter_status'), data.get('page'),
                                                                     data.get('size'))

    @staticmethod
    def get_detail_absensi_borongan(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        approval = ApprovalAbsensiBoronganRepository.get_detail_by_id(approval_id)

        if not approval:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})
        return approval

    @staticmethod
    def cancel_absensi_borongan(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={
                                                    'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalAbsensiBoronganRepository.get_detail_by_id_and_user_id(user.id, approval_id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={
                                                    'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})

            absensi_to_cancel = AbsensiBoronganRepository.get_detail_by_id(approval.absensi_borongan_id)
            if not absensi_to_cancel:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={
                                                    'resource': AppConstants.ABSENSI_BORONGAN_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.CANCELLATION_NOT_ALLOWED)

            ApprovalAbsensiBoronganRepository.delete(approval)
            AbsensiBoronganRepository.delete(absensi_to_cancel)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_approval_by_pic_id(pic_username, request):

        user = UserRepository.get_user_by_username(pic_username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})
        return ApprovalAbsensiBoronganRepository.get_list_pagination_approval_user(user.id, request.get('page'),
                                                                                   request.get('size'),
                                                                                   request.get('filter_month'),
                                                                                   request.get('filter_status'))

    @staticmethod
    def get_detail_by_approval_user(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        approval = ApprovalAbsensiBoronganRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)
        if not approval:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_REIMBURSE_RESOURCE.value})

        return approval

    @staticmethod
    def approve_absensi_borongan(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalAbsensiBoronganRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.APPROVAL_LEMBUR_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.APPROVED.value
            approval.absensi_borongan.status = AppConstants.APPROVED.value

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.APPROVE_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value}),
                                                         format_string(AppConstants.APPROVE_BODY.value, params={
                                                             'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value,
                                                             'nama_pengaju': approval.approval_user.fullname
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def reject_absensi_borongan(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalAbsensiBoronganRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={
                                                    'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.REJECTED.value
            approval.absensi_borongan.status = AppConstants.REJECTED.value

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.REJECT_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value}),
                                                         format_string(AppConstants.REJECT_BODY.value, params={
                                                             'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value,
                                                             'nama_pengaju': approval.approval_user.fullname
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e
