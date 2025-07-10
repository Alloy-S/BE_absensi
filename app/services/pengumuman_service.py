from app.repositories.user_repository import UserRepository
from app.repositories.pengumuman_repository import PengumumanRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam

class PengumumanService:

    @staticmethod
    def get_pengumuman_by_id(pengumuman_id):

        return PengumumanRepository.get_by_id(pengumuman_id)

    @staticmethod
    def get_all_pagination_user(page, size, search):
        return PengumumanRepository.get_all_pagination_user(page=page, per_page=size, search=search)

    @staticmethod
    def get_all_pagination_admin(page, size, search):
        return PengumumanRepository.get_all_pagination_admin(page=page, per_page=size, search=search)

    @staticmethod
    def create_pengumuman(username, data):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})


        data['created_by'] = user.id

        new_pengumuman = PengumumanRepository.create_pengumuman(data)

        return new_pengumuman

    @staticmethod
    def edit_pengumuman(pengumuman_id, data, username):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        pengumuman = PengumumanRepository.get_by_id(pengumuman_id)

        if not pengumuman:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.PENGUMUMAN_RESOURCE.value})

        return PengumumanRepository.edit_pengumuman(pengumuman, data, user.id)

    @staticmethod
    def delete_pengumuman_by_id(pengumuman_id):
        pengumuman = PengumumanRepository.get_by_id(pengumuman_id)

        if not pengumuman:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.PENGUMUMAN_RESOURCE.value})

        PengumumanRepository.delete_pengumuman(pengumuman)


