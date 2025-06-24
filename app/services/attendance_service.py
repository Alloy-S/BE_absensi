from datetime import date, datetime, timedelta
from geopy.distance import geodesic
from app.database import db
from app.repositories.absensi_repository import AbsensiRepository
from app.repositories.detail_absensi_repository import DetailAbsensiRepository
from app.services.face_recognition_service import FaceRecognitionService
from app.repositories.user_repository import UserRepository
from app.repositories.libur_repository import LiburRepository
from app.repositories.detail_jadwal_kerja_repository import DetailJadwalKerjaRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.services.libur_service import LiburService
from app.utils.error_code import ErrorCode
from app.utils.app_constans import AppConstants
from app.entity.detail_jadwal_kerja import DetailJadwalKerja


class AttendanceService:

    @staticmethod
    def _verify_location(user, current_latitude, current_longitude) -> bool:

        if not user.data_karyawan or not user.data_karyawan.lokasi:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.LOCATION.value})

        work_location = user.data_karyawan.lokasi

        user_coords = (current_latitude, current_longitude)
        work_coords = (work_location.latitude, work_location.longitude)

        distance = geodesic(user_coords, work_coords).meters

        return distance <= work_location.toleransi

    @staticmethod
    def create_attendance(username: str, data, image_path):
        try:
            today = datetime.today()
            attendance_type = data["type"]

            # cek user valid
            user = UserRepository.get_user_by_username(username)
            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            # cek apakah hari libur
            libur = LiburRepository.get_libur_by_date(today.date())

            if libur:
                raise GeneralException(ErrorCode.TODAY_IS_HOLIDAY)

            # cek lokasi
            is_location_valid = AttendanceService._verify_location(user, data['latitude'], data['longitude'])
            if not is_location_valid:
                raise GeneralException(ErrorCode.USER_LOCATION_NOT_MATCH_REQUIREMENT)

            # # cek wajah
            is_face_valid = FaceRecognitionService.verify_face(user_id=user.id, image_path=image_path)
            if not is_face_valid:
                raise GeneralException(ErrorCode.USER_FACE_NOT_MATCH_REQUIREMENT)

            # cek jadwal kerja
            jadwal_kerja = user.data_karyawan.jadwal_kerja

            detail_jadwal = DetailJadwalKerjaRepository.get_detail_jadwal_kerja_by_jadwal_id_and_hari(jadwal_kerja.id,
                                                                                                      today.strftime(
                                                                                                          "%A").upper())

            if not detail_jadwal:
                raise GeneralException(ErrorCode.TODAY_IS_HOLIDAY)

            print(detail_jadwal.time_in)

            # cek waktu kehadiran
            status = AttendanceService.check_attendance_time(attendance_type, detail_jadwal, today)

            # save data presensi
            absensi = AbsensiRepository.get_absensi_by_user_id_and_date(user_id=user.id, date=today.date())

            if not absensi:
                absensi = AbsensiRepository.create_absensi({
                    'date': today.date(),
                    'lokasi': user.data_karyawan.lokasi.name,
                    'metode': AppConstants.FACE_RECOGNITION.value,
                    'status': status,
                    'user_id': user.id
                })

            DetailAbsensiRepository.delete_detail_absensi_by_absensi_id_and_type(absensi.id, attendance_type)
            DetailAbsensiRepository.create_detail_absensi({
                'absensi_id': absensi.id,
                'date': today,
                'type': attendance_type,
                'status_appv': AppConstants.APPROVED.value,
                'status_absensi': status,
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'catatan': data.get('catatan', ""),
            })

            db.session.commit()

            return status
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def check_attendance_time(attendance_type, detail_jadwal: DetailJadwalKerja, today):

        print(detail_jadwal.time_in)
        status = ""
        if attendance_type == AppConstants.ATTENDANCE_IN.value:
            scheduled_check_in = datetime.combine(today.date(), detail_jadwal.time_in)
            late_deadline = scheduled_check_in + timedelta(minutes=detail_jadwal.toler_in)

            if today <= scheduled_check_in:
                status = AppConstants.ON_TIME.value
            elif scheduled_check_in < today <= late_deadline:
                status = AppConstants.LATE.value
            else:
                status = AppConstants.LATE.value

        elif attendance_type == AppConstants.ATTENDANCE_OUT.value:
            scheduled_check_out = datetime.combine(today.date(), detail_jadwal.time_out)
            early_leave_deadline = scheduled_check_out - timedelta(minutes=detail_jadwal.toler_out)

            if today >= early_leave_deadline:
                status = AppConstants.ON_TIME.value
            else:
                status = AppConstants.EARLY.value
        else:
            raise GeneralException(ErrorCode.ATTENDANCE_TYPE_NOT_VALID)
        return status


    @staticmethod
    def check_today_attendance(username):
        today = datetime.today()
        status = None
        required_attendance_type = None

        # cek user valid
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        if LiburRepository.get_libur_by_date(today.date()):
            status = AppConstants.HOLIDAY.value
        else:
            # cek jadwal kerja
            jadwal_kerja = user.data_karyawan.jadwal_kerja

            detail_jadwal = DetailJadwalKerjaRepository.get_detail_jadwal_kerja_by_jadwal_id_and_hari(jadwal_kerja.id,
                                                                                                      today.strftime(
                                                                                                          "%A").upper())

            if not detail_jadwal:
                status = AppConstants.HOLIDAY.value

        if status == AppConstants.HOLIDAY.value:
            return {
                'status': status,
                'required_attendance_type': None
            }

        absensi = AbsensiRepository.get_absensi_by_user_id_and_date(user_id=user.id, date=today.date())

        if not absensi:

            required_attendance_type = AppConstants.ATTENDANCE_IN.value
        else:
            has_checked_in = DetailAbsensiRepository.get_detail_absensi_by_absensi_id_and_type_and_status_appv(
                absensi.id, AppConstants.ATTENDANCE_IN.value, AppConstants.APPROVED.value
            ) is not None

            has_checked_out = DetailAbsensiRepository.get_detail_absensi_by_absensi_id_and_type_and_status_appv(
                absensi.id, AppConstants.ATTENDANCE_OUT.value, AppConstants.APPROVED.value
            ) is not None

            if has_checked_in and has_checked_out:
                required_attendance_type = None
            elif has_checked_in:
                required_attendance_type = AppConstants.ATTENDANCE_OUT.value
            else:
                required_attendance_type = AppConstants.ATTENDANCE_IN.value

        response = {
            'status': status,
            'required_attendance_type': required_attendance_type,
        }

        return response



