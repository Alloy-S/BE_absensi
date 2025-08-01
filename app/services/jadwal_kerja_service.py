from app.utils.app_constans import AppConstants
from app.execption.custom_execption import GeneralExceptionWithParam
from app.repositories.jadwal_kerja_repository import JadwalKerjaRepository
from app.utils.error_code import ErrorCode


class JadwalKerjaService:
    @staticmethod
    def get_all():
        return JadwalKerjaRepository.get_all()

    @staticmethod
    def get_all_pagination(page, size, search):
        return JadwalKerjaRepository.get_all_pagination(page=page, size=size, search=search)
    
    @staticmethod
    def get_by_id(id):
        return JadwalKerjaRepository.get_by_id(id)
    
    @staticmethod
    def create(kode, shift, details: list):
        jadwal = JadwalKerjaRepository.get_by_kode(kode=kode)
    
        if jadwal:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE,
                                                params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        return JadwalKerjaRepository.create(kode, shift, details)
    
    @staticmethod
    def update(id, kode, shift, details: list):
        jadwal = JadwalKerjaRepository.get_by_id(id)
        if not jadwal:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        return JadwalKerjaRepository.update(jadwal, kode, shift, details)
    
    @staticmethod
    def delete(id):
        jadwal = JadwalKerjaRepository.get_by_id(id)
        if not jadwal:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        JadwalKerjaRepository.delete(jadwal_kerja=jadwal)
        return True