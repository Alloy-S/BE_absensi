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
    def get_by_id(jadwal_id):
        return JadwalKerjaRepository.get_by_id(jadwal_id)
    
    @staticmethod
    def create_jadwal(kode, shift, details: list):
        jadwal = JadwalKerjaRepository.get_by_kode(kode=kode)
    
        if jadwal:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE,
                                                params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        return JadwalKerjaRepository.create_jadwal(kode, shift, details)
    
    @staticmethod
    def create_new_jadwal_copy(jadwal_id, data):
        old_jadwal = JadwalKerjaRepository.get_by_id(jadwal_id)
        if not old_jadwal:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        return JadwalKerjaRepository.create_new_version(old_jadwal, data.get('kode'), data.get('shift'), data.get('detail_jadwal_kerja'), data.get('migrate_data'))
    
    @staticmethod
    def non_aktif_jadwal(jadwal_id):
        jadwal = JadwalKerjaRepository.get_by_id(jadwal_id)
        if not jadwal:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        JadwalKerjaRepository.non_aktif_jadwal(jadwal_kerja=jadwal)
        return True

    @staticmethod
    def aktif_jadwal(jadwal_id):
        jadwal = JadwalKerjaRepository.get_by_id(jadwal_id)
        if not jadwal:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JADWAL_KERJA_RESOURCE.value})
        JadwalKerjaRepository.aktif_jadwal(jadwal_kerja=jadwal)
        return True