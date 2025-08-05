import base64
import uuid
import os
import math
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
    def hitung_jarak_haversine(lat1, lon1, lat2, lon2):
        R = 6371000

        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        jarak = R * c

        return jarak

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
    def create_attendance(username: str, data):
        try:
            base64_string = data['image']

            try:
                if "," in base64_string:
                    _, base64_data = base64_string.split(",", 1)
                else:
                    base64_data = base64_string

                image_data = base64.b64decode(base64_data)
            except (ValueError, TypeError):
                raise GeneralException(ErrorCode.INVALID_BASE64)

            filename = f"{uuid.uuid4()}.jpg"
            temp_path = os.path.join(AppConstants.UPLOAD_FOLDER.value, filename)

            with open(temp_path, 'wb') as f:
                f.write(image_data)

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
            is_face_valid = FaceRecognitionService.verify_face(user_id=user.id, image_path=temp_path)
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
                    'user_id': user.id,
                    'jadwal_time_in': detail_jadwal.time_in,
                    'jadwal_time_out': detail_jadwal.time_out,
                    'jadwal_toler_in': detail_jadwal.toler_in,
                    'jadwal_toler_out': detail_jadwal.toler_out,
                    'jadwal_kerja_id': jadwal_kerja.id,
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
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    @staticmethod
    def check_attendance_time(attendance_type: str, detail_jadwal: DetailJadwalKerja, current_datetime: datetime):
        status = ""
        time_in = detail_jadwal.time_in
        time_out = detail_jadwal.time_out

        is_overnight_shift = time_out < time_in

        if attendance_type == AppConstants.ATTENDANCE_IN.value:
            scheduled_check_in = datetime.combine(current_datetime.date(), time_in)
            late_deadline = scheduled_check_in + timedelta(minutes=detail_jadwal.toler_in)

            if current_datetime <= scheduled_check_in:
                status = AppConstants.ON_TIME.value
            elif scheduled_check_in < current_datetime <= late_deadline:
                status = AppConstants.LATE.value
            else:
                status = AppConstants.LATE.value

        elif attendance_type == AppConstants.ATTENDANCE_OUT.value:
            if is_overnight_shift and current_datetime.time() < time_out:
                work_date = current_datetime.date() - timedelta(days=1)
            else:
                work_date = current_datetime.date()

            checkout_date = work_date + timedelta(days=1) if is_overnight_shift else work_date

            scheduled_check_out = datetime.combine(checkout_date, time_out)
            early_leave_deadline = scheduled_check_out - timedelta(minutes=detail_jadwal.toler_out)

            if current_datetime >= scheduled_check_out:
                status = AppConstants.ON_TIME.value
            elif early_leave_deadline <= current_datetime < scheduled_check_out:
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
        time_clock_in = None
        time_clock_out = None
        shift_info = ""


        user = UserRepository.get_user_by_username(username)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})


        if LiburRepository.get_libur_by_date(today.date()):
            status = AppConstants.HOLIDAY.value
            return {
                'status': status,
                'required_attendance_type': None,
                'time_clock_in': None,
                'time_clock_out': None,
                'today': today.date(),
                'shift': "Hari Libur Nasional",
            }

        if not user.data_karyawan.jadwal_kerja:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})

        jadwal_kerja = user.data_karyawan.jadwal_kerja

        detail_jadwal = DetailJadwalKerjaRepository.get_detail_jadwal_kerja_by_jadwal_id_and_hari(
            jadwal_kerja.id, today.strftime("%A").upper()
        )


        if not detail_jadwal or not detail_jadwal.is_active:
            status = AppConstants.HOLIDAY.value
            return {
                'status': status,
                'required_attendance_type': None,
                'time_clock_in': None,
                'time_clock_out': None,
                'today': today.date(),
                'shift': "Hari Libur",
            }

        shift_info = f"{jadwal_kerja.shift} ({detail_jadwal.time_in} - {detail_jadwal.time_out})"

        yesterday = today - timedelta(days=1)
        jadwal_kemarin = DetailJadwalKerjaRepository.get_detail_jadwal_kerja_by_jadwal_id_and_hari(
            jadwal_kerja.id, yesterday.strftime("%A").upper()
        )

        absensi = None

        if jadwal_kemarin and jadwal_kemarin.time_out < jadwal_kemarin.time_in:

            scheduled_checkout_yesterday = datetime.combine(today.date(), jadwal_kemarin.time_out)
            checkout_window_end = scheduled_checkout_yesterday + timedelta(hours=2)

            if today <= checkout_window_end:
                absensi_kemarin = AbsensiRepository.get_absensi_by_user_id_and_date(user.id, yesterday.date())
                if absensi_kemarin:
                    detail_out_kemarin = DetailAbsensiRepository.get_detail_by_absensi_id_and_type(absensi_kemarin.id,
                                                                                                   AppConstants.ATTENDANCE_OUT.value)
                    if not detail_out_kemarin:
                        absensi = absensi_kemarin

        if not absensi:
            absensi = AbsensiRepository.get_absensi_by_user_id_and_date(user.id, today.date())

        if not absensi:
            required_attendance_type = AppConstants.ATTENDANCE_IN.value
        else:

            detail_in = DetailAbsensiRepository.get_detail_by_absensi_id_and_type(absensi.id,
                                                                                  AppConstants.ATTENDANCE_IN.value)
            detail_out = DetailAbsensiRepository.get_detail_by_absensi_id_and_type(absensi.id,
                                                                                   AppConstants.ATTENDANCE_OUT.value)

            if detail_in:
                time_clock_in = detail_in.date
            if detail_out:
                time_clock_out = detail_out.date


            if detail_in and detail_out:
                required_attendance_type = None
            elif detail_in:
                required_attendance_type = AppConstants.ATTENDANCE_OUT.value
            else:
                required_attendance_type = AppConstants.ATTENDANCE_IN.value


        return {
            'status': AppConstants.WORK.value,
            'required_attendance_type': required_attendance_type,
            'time_clock_in': time_clock_in,
            'time_clock_out': time_clock_out,
            'today': today.date(),
            'shift': shift_info,
        }



