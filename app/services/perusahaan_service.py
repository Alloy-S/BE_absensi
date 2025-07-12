from app.entity import Perusahaan
from app.repositories.user_repository import UserRepository
from app.repositories.perusahaan_repository import PerusahaanRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam


class PerusahaanService:

    @staticmethod
    def get_profile_perusahaan():
        return PerusahaanRepository.get_profile_perusahaan()

    @staticmethod
    def edit_profile_perusahaan(username, data):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        perusahaan = PerusahaanRepository.get_profile_perusahaan()

        result = PerusahaanRepository.edit_profile_perusahaan(perusahaan, data, user.id)

        return result