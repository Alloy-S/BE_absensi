from app import AppConstants
from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.jabatan_repository import JabatanRepository
from app.utils.error_code import ErrorCode


class JabatanService:
    @staticmethod
    def get_all_pagination(page, size, search):
        return JabatanRepository.get_all_pagination(page=page, per_page=size, search=search)
    
    @staticmethod
    def get_all():
        return JabatanRepository.get_all()
    
    @staticmethod
    def create(nama, parent_id):
        
        jabatan = JabatanRepository.get_by_name(nama)
        
        if jabatan:
            raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={"resource": AppConstants.JABATAN_RESOURCE.value})
        
        return JabatanRepository.create(nama=nama, parent_id=parent_id)
    
    @staticmethod
    def get_by_id(id):
        jabatan = JabatanRepository.get_by_id(id)

        if not jabatan:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={"resource": AppConstants.JABATAN_RESOURCE.value})

        return jabatan
    
    @staticmethod
    def update(id, nama, parent_id):
        jabatan = JabatanRepository.get_by_id(id)
        
        if not jabatan:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={"resource": AppConstants.JABATAN_RESOURCE.value})

        if jabatan.nama != nama:
            if JabatanRepository.get_by_name(nama):
                raise GeneralExceptionWithParam(ErrorCode.DUPLICATE_RESOURCE, params={"resource": AppConstants.JABATAN_RESOURCE.value})
        
        jabatan_updated = JabatanRepository.update_jabatan(jabatan, nama, parent_id)
        
        return jabatan_updated
    
    @staticmethod
    def delete(id):
        jabatan = JabatanRepository.get_by_id(id)

        if not jabatan:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={"resource": AppConstants.JABATAN_RESOURCE.value})

        if jabatan.children:
            raise GeneralException(ErrorCode.DELETION_NOT_ALLOWED)

        if jabatan.data_karyawan:
            raise GeneralException(ErrorCode.DELETION_NOT_ALLOWED)

        return JabatanRepository.delete_jabatan(jabatan)