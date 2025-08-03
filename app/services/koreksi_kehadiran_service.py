from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.approval_koreksi_repository import ApprovalKoreksiRepository
from app.repositories.absensi_repository import AbsensiRepository
from app.repositories.detail_absensi_repository import DetailAbsensiRepository
from app.repositories.user_repository import UserRepository
from app.repositories.detail_jadwal_kerja_repository import DetailJadwalKerjaRepository
from app.repositories.detail_approval_koreksi_repository import DetailApprovalKoreksiRepository
from app.services.attendance_service import AttendanceService
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db
from datetime import datetime
from app.utils.global_utils import format_string


class KoreksiKehadiranService:

    @staticmethod
    def get_list_koreksi(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalKoreksiRepository.get_list_pagination(user.id, request.get("page"), request.get("size"),
                                                             request.get("filter_month"), request.get("filter_status"))

    @staticmethod
    def get_list_koreksi_approval_user(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        return ApprovalKoreksiRepository.get_list_pagination_approval_user(user.id, request.get("page"),
                                                                           request.get("size"),
                                                                           request.get("filter_month"),
                                                                           request.get("filter_status"))

    @staticmethod
    def get_detail_koreksi(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalKoreksiRepository.get_detail_by_id_and_user_id(user.id, approval_id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.ABSENSI_RESOURCE.value})
        return result

    @staticmethod
    def get_detail_koreksi_by_approval_user(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        result = ApprovalKoreksiRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)
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

        koreksi_to_cancel = ApprovalKoreksiRepository.get_detail_by_id_and_user_id(user.id, approval_id)

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

    @staticmethod
    def approve_koreksi(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalKoreksiRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.APPROVAL_KOREKSI_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            absensi_date = approval.absensi_date
            absensi = None

            detail_koreksi = approval.detail_approval

            detail_in = None
            detail_out = None

            for detail in detail_koreksi:
                if detail.type == AppConstants.ATTENDANCE_IN.value:
                    detail_in = detail
                elif detail.type == AppConstants.ATTENDANCE_OUT.value:
                    detail_out = detail

            detail_jadwal_kerja = DetailJadwalKerjaRepository.get_detail_jadwal_kerja_by_jadwal_id_and_hari(
                approval.user.data_karyawan.jadwal_kerja.id, absensi_date.strftime(
                    "%A").upper())

            if approval.absensi:
                print("Koreksi Absensi History")
                absensi = approval.absensi

                DetailAbsensiRepository.delete_detail_absensi_by_absensi_id(absensi.id)

            else:
                print("Koreksi Absensi Baru")

                absensi = AbsensiRepository.create_absensi({
                    'date': absensi_date,
                    'lokasi': user.data_karyawan.lokasi.name,
                    'metode': AppConstants.FACE_RECOGNITION.value,
                    'status': AppConstants.ON_TIME.value,
                    'user_id': user.id
                })

            status_in = AttendanceService.check_attendance_time(AppConstants.ATTENDANCE_IN.value, detail_jadwal_kerja,
                                                                detail_in.requested_datetime)
            status_out = AttendanceService.check_attendance_time(AppConstants.ATTENDANCE_OUT.value, detail_jadwal_kerja,
                                                                 detail_out.requested_datetime)

            final_status = ""

            if status_in == AppConstants.LATE.value and status_out == AppConstants.EARLY.value:
                final_status = AppConstants.LATE_AND_EARLY.value
            elif status_out == AppConstants.EARLY.value:
                final_status = AppConstants.EARLY.value
            elif status_in == AppConstants.LATE.value:
                final_status = AppConstants.LATE.value
            else:
                final_status = AppConstants.ON_TIME.value

            absensi.status = final_status
            absensi.metode = AppConstants.KOREKSI_KEHADIRAN.value

            DetailAbsensiRepository.create_detail_absensi({
                'absensi_id': absensi.id,
                'date': detail_in.requested_datetime,
                'type': AppConstants.ATTENDANCE_IN.value,
                'status_appv': AppConstants.APPROVED.value,
                'status_absensi': status_in,
                'latitude': None,
                'longitude': None,
                'catatan': "",
            })

            DetailAbsensiRepository.create_detail_absensi({
                'absensi_id': absensi.id,
                'date': detail_out.requested_datetime,
                'type': AppConstants.ATTENDANCE_OUT.value,
                'status_appv': AppConstants.APPROVED.value,
                'status_absensi': status_out,
                'latitude': None,
                'longitude': None,
                'catatan': "",
            })

            approval.status = AppConstants.APPROVED.value

            db.session.commit()

            NotificationService.send_single_notification(approval.user.fcm_token,
                                                         format_string(AppConstants.APPROVE_TITLE.value,
                                                                       params={
                                                                           'resource': AppConstants.KOREKSI_KEHADIRAN.value}),
                                                         format_string(AppConstants.APPROVE_BODY.value, params={
                                                             'resource': AppConstants.IZIN_RESOURCE.value,
                                                             'nama_pengaju': approval.approval_user.fullname
                                                         }))

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def reject_koreksi(username, approval_id):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            approval = ApprovalKoreksiRepository.get_detail_by_id_and_approval_user_id(approval_id, user.id)

            if not approval:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.APPROVAL_KOREKSI_RESOURCE.value})

            if approval.status != AppConstants.WAITING_FOR_APPROVAL.value:
                raise GeneralException(ErrorCode.APPROVER_NOT_ALLOWED)

            approval.status = AppConstants.REJECTED.value

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
