from app.repositories.grup_gaji_repository import GrupGajiRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.repositories.kode_perhitungan_repository import KodePerhitunganRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db

class GrupGajiService:
    @staticmethod
    def create_grup_gaji(data):
        existing_grup_gaji = GrupGajiRepository.get_grup_gaji_by_kode(data.get("grup_kode"))

        if existing_grup_gaji:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={'resource': AppConstants.GRUP_GAJI.value})

        try:
            new_grup_gaji = GrupGajiRepository.create_grup_gaji(data)

            GrupGajiRepository.delete_and_insert_grup_gaji_kom(new_grup_gaji, data.get('komponen', []))

            db.session.commit()
            return new_grup_gaji
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_grup_gaji_by_id(grup_id):
        result = GrupGajiRepository.get_grup_gaji_by_id(grup_id)
        if not result:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.GRUP_GAJI.value})
        return result

    @staticmethod
    def get_paginated_grup_gaji(request):
        return GrupGajiRepository.get_all_grup_gaji_paginated(request.get('page'), request.get('size'), request.get('search'))

    @staticmethod
    def update_grup_gaji(grup_id, data):
        grup_gaji = GrupGajiRepository.get_grup_gaji_by_id(grup_id)
        if not grup_gaji:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.GRUP_GAJI.value})

        existing_grup_gaji = GrupGajiRepository.get_grup_gaji_by_kode(data.get("grup_kode"))

        if existing_grup_gaji and grup_gaji.id != existing_grup_gaji.id:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={'resource': AppConstants.GRUP_GAJI.value})

        try:
            GrupGajiRepository.update_grup_gaji(grup_gaji, data)

            GrupGajiRepository.delete_and_insert_grup_gaji_kom(grup_gaji, data.get('komponen', []))

            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def delete_grup_gaji(grup_id):
        grup_gaji = GrupGajiRepository.get_grup_gaji_by_id(grup_id)
        if not grup_gaji:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.GRUP_GAJI.value})

        try:
            GrupGajiRepository.delete_grup_gaji(grup_gaji)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_all_kode_perhitungan():
        return KodePerhitunganRepository.get_all_kode_perhitungan()

    @staticmethod
    def get_all_grup_gaji():
        return GrupGajiRepository.get_all_grup_gaji()

    @staticmethod
    def get_grup_gaji_users(grup_gaji_id):
        grup_gaji = GrupGajiRepository.get_grup_gaji_by_id(grup_gaji_id)

        if not grup_gaji:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.GRUP_GAJI.value})

        list_karyawan = GrupGajiRepository.get_grup_gaji_users(grup_gaji_id)

        return {
            'grup_gaji': grup_gaji,
            'list_karyawan': list_karyawan,
        }