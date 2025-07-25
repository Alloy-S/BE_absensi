from app.repositories.jatah_cuti_repository import JatahCutiRepository
from app.repositories.user_repository import UserRepository
from app.repositories.jenis_izin_repository import JenisIzinRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db
from datetime import date
from dateutil.relativedelta import relativedelta

class JatahCutiService:
    @staticmethod
    def create_jatah_cuti(user_id, data):
        existing = JatahCutiRepository.find_by_user_and_type(
            user_id, data['jenis_izin_id'], data['periode']
        )
        if existing:
            raise GeneralException(ErrorCode.EXISTING_KUOTA_CUTI)

        return JatahCutiRepository.create(user_id, data)

    @staticmethod
    def get_list_for_user(user_id, page, size):
        user = UserRepository.get_user_by_id(user_id)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.USER_RESOURCE.value})

        pagination = JatahCutiRepository.get_list_pagination_for_user(user_id, page, size)

        response = {
            "user": user,
            "pages": pagination.pages,
            "total": pagination.total,
            "items": pagination.items
        }

        return response

    @staticmethod
    def get_detail(jatah_cuti_id):
        jatah_cuti = JatahCutiRepository.get_by_id(jatah_cuti_id)
        if not jatah_cuti:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.KUOTA_CUTI_RESOURCE.value})
        return jatah_cuti

    @staticmethod
    def adjust_kuota(jatah_cuti_id, data):
        jatah_cuti = JatahCutiService.get_detail(jatah_cuti_id)
        return JatahCutiRepository.update(jatah_cuti, data)

    @staticmethod
    def delete_jatah_cuti(jatah_cuti_id):
        jatah_cuti = JatahCutiService.get_detail(jatah_cuti_id)

        if jatah_cuti.kuota_terpakai > 0:
            raise GeneralException(ErrorCode.CUTI_INUSE)
        return JatahCutiRepository.delete(jatah_cuti)

    @staticmethod
    def generate_kuota_tahunan(target_year: int):
        try:
            active_users = UserRepository.get_all_active_users()
            annual_leave_types = JenisIzinRepository.find_by_reset_period('TAHUNAN')

            for user in active_users:
                if not user.data_karyawan or not user.data_karyawan.tgl_gabung:
                    continue

                join_date = user.data_karyawan.tgl_gabung
                start_of_year = date(target_year, 1, 1)

                delta = relativedelta(start_of_year, join_date)
                masa_kerja_bulan = delta.months + delta.years * 12

                for izin_type in annual_leave_types:
                    if masa_kerja_bulan >= izin_type.berlaku_setelah_bulan:
                        existing_jatah = JatahCutiRepository.find_by_user_and_type(user.id, izin_type.id, target_year)
                        if not existing_jatah:
                            jatah_payload = {
                                'jenis_izin_id': izin_type.id,
                                'periode': target_year,
                                'kuota_awal': izin_type.kuota_default
                            }

                            JatahCutiRepository.create(
                                user_id=user.id,
                                data=jatah_payload
                            )


            db.session.commit()
            return {"message": f"Kuota cuti untuk tahun {target_year} berhasil dibuat."}

        except Exception as e:
            db.session.rollback()
            raise e