from app.repositories.komponen_gaji_repository import KomponenGajiRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db

class KomponenGajiService:

    @staticmethod
    def create_kom_gaji(data):
        kom_gaji = KomponenGajiRepository.get_kom_gaji_by_kode(data['kom_kode'])

        if kom_gaji:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={'resource': AppConstants.KOMPONEN_GAJI_RESOURCE.value})

        return KomponenGajiRepository.create_kom_gaji(data)

    @staticmethod
    def get_kom_gaji_by_id(kom_gaji_id):
        kom_gaji = KomponenGajiRepository.get_kom_gaji_by_id(kom_gaji_id)

        if not kom_gaji:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.KOMPONEN_GAJI_RESOURCE.value})

        return kom_gaji

    @staticmethod
    def update_kom_gaji(kom_gaji_id, data):
        kom_gaji_old = KomponenGajiRepository.get_kom_gaji_by_id(kom_gaji_id)

        if not kom_gaji_old:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.KOMPONEN_GAJI_RESOURCE.value})

        existing_kom_gaji = KomponenGajiRepository.get_kom_gaji_by_kode(data['kom_kode'])

        if existing_kom_gaji and existing_kom_gaji.id != kom_gaji_old.id:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE,
                                      params={'resource': AppConstants.KOMPONEN_GAJI_RESOURCE.value})

        return KomponenGajiRepository.update_kom_gaji(kom_gaji_old, data)

    @staticmethod
    def get_kom_gaji_pagination(request):
        return KomponenGajiRepository.get_kom_gaji_pagination(request.get('search'), request.get('page'), request.get('size'))

    @staticmethod
    def delete_kom_gaji(kom_gaji_id):
        kom_gaji = KomponenGajiRepository.get_kom_gaji_by_id(kom_gaji_id)

        if not kom_gaji:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.KOMPONEN_GAJI_RESOURCE.value})

        if kom_gaji.grup_gaji_kom:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_IN_USE,
                                            params={'resource': AppConstants.KOMPONEN_GAJI_RESOURCE.value})

        KomponenGajiRepository.delete_kom_gaji(kom_gaji)

    @staticmethod
    def get_all_kom_gaji():
        return KomponenGajiRepository.get_all_kom_gaji()

