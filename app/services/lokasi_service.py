from app.utils.app_constans import AppConstants
from app.execption.custom_execption import GeneralExceptionWithParam
from app.repositories.lokasi_repository import LokasiRepository
from app.utils.error_code import ErrorCode


class LokasiService:
    @staticmethod
    def get_all_lokasi():
        return LokasiRepository.get_all_lokasi()

    @staticmethod
    def get_all_lokasi_pagination(page, size, search):
        return LokasiRepository.get_all_pagination(page=page, per_page=size, search=search)
    
    @staticmethod
    def get_lokasi_by_id(id):
        return LokasiRepository.get_lokasi_by_id(id)
    
    @staticmethod
    def create_lokasi(name , latitude, longitude, toleransi):
        print("========== ADD NEW LOKASI")
        lokasi = LokasiRepository.get_lokasi_by_name(name=name)
        
        if lokasi:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE,
                                            params={'resource': AppConstants.LOKASI_RESOURCE.value})
        return LokasiRepository.create_lokasi(name , latitude, longitude, toleransi)
    
    @staticmethod
    def update_lokasi(id, name, latitude, longitude, toleransi):
        lokasi = LokasiRepository.get_lokasi_by_id(id)
        if not lokasi:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.LOKASI_RESOURCE.value})
        return LokasiRepository.update_lokasi(lokasi, name, latitude, longitude, toleransi)
    
    @staticmethod
    def delete_lokasi(id):
        lokasi = LokasiRepository.get_lokasi_by_id(id)
        if not lokasi:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.LOKASI_RESOURCE.value})
        LokasiRepository.delete_lokasi(lokasi)