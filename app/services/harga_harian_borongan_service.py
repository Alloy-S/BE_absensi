from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.harga_harian_borongan_repository import HargaHarianBoronganRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db

class HargaHarianBoronganService:

    @staticmethod
    def get_all_harga_harian_borongan():
        return HargaHarianBoronganRepository.get_all_harga_active()

    @staticmethod
    def get_harga_pagination(page, size, search):
        return HargaHarianBoronganRepository.get_harga_pagination(page, size, search)

    @staticmethod
    def get_harga_by_id(harga_id):
        return HargaHarianBoronganRepository.get_harga_by_id(harga_id)

    @staticmethod
    def get_harga_by_grup(grup_id):
        return HargaHarianBoronganRepository.get_harga_by_harga_grup(grup_id)

    @staticmethod
    def create_new_harga(data):
        new_harga = HargaHarianBoronganRepository.create_harga(data)
        db.session.commit()
        return new_harga

    @staticmethod
    def edit_harga(harga_id, data):
        harga = HargaHarianBoronganRepository.get_harga_by_id(harga_id)

        if not harga:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.HARGA_RESOURCE.value})

        data['grup_id'] = harga.grup_id
        new_harga = HargaHarianBoronganRepository.update_harga(data)

        HargaHarianBoronganRepository.non_active_harga(harga)

        db.session.commit()

        return new_harga

    @staticmethod
    def non_active_harga(harga_id):
        harga = HargaHarianBoronganRepository.get_harga_by_id(harga_id)

        if not harga:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.HARGA_RESOURCE.value})

        if harga.detail_absensi_borongan:
            raise GeneralException(ErrorCode.DELETION_NOT_ALLOWED)

        HargaHarianBoronganRepository.non_active_harga(harga)
        db.session.commit()
