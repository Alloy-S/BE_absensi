from app.repositories.jenis_izin_repository import JenisIzinRepository
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.database import db


class JenisIzinService:
    @staticmethod
    def create_jenis_izin(data):
        if JenisIzinRepository.find_by_name(data['nama']):
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={'resource': AppConstants.JENIS_IZIN_RESOURCE.value})
        return JenisIzinRepository.create(data)

    @staticmethod
    def get_jenis_izin_pagination(page, size, search):
        return JenisIzinRepository.get_list_pagination(page, size, search)

    @staticmethod
    def get_jenis_izin_all():
        return JenisIzinRepository.get_all()

    @staticmethod
    def get_jenis_izin_by_id(jenis_izin_id):
        jenis_izin = JenisIzinRepository.get_by_id(jenis_izin_id)
        if not jenis_izin:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.JENIS_IZIN_RESOURCE.value})
        return jenis_izin

    @staticmethod
    def update_jenis_izin(jenis_izin_id, data):
        jenis_izin = JenisIzinService.get_jenis_izin_by_id(jenis_izin_id)
        if data['nama'] != jenis_izin.nama and JenisIzinRepository.find_by_name(data['nama']):
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={'resource':  AppConstants.JENIS_IZIN_RESOURCE.value})
        return JenisIzinRepository.update(jenis_izin, data)

    @staticmethod
    def delete_jenis_izin(jenis_izin_id):
        jenis_izin = JenisIzinService.get_jenis_izin_by_id(jenis_izin_id)
        if jenis_izin.jatah_kuota_cuti or jenis_izin.izin:
            raise GeneralException(ErrorCode.DELETION_NOT_ALLOWED)
        return JenisIzinRepository.delete(jenis_izin)