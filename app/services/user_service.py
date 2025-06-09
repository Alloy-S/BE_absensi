from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.user_repository import UserRepository
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.utils.global_utils import generate_password, generate_username
from app.repositories.data_karyawan_repository import DataKaryawanRepository


class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_users_pagination(page, per_page, search):
        return UserRepository.get_users_pagination(page=page, per_page=per_page, search=search)

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def get_user_by_username(username):
        return UserRepository.get_user_by_username(username)

    @staticmethod
    def create_user(fullname, data_pribadi, data_kontak, data_karyawan):

        username = generate_username()
        password = generate_password()

        nip = DataKaryawanRepository.generate_new_nip()

        result = UserRepository.create_user(fullname, username, password, data_pribadi, data_kontak, data_karyawan, nip)

        try:
            NotificationService.send_notification_login_data(phone=result.phone, username=username, password=password, fullname=fullname, nip=nip)
        except Exception as e:
            print(f"Sending notification failed: {str(e)}")

        return None

    @staticmethod
    def update_user(user_id, data):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.USER_RESOURCE.value})
        UserRepository.update_user(user, data)
        return None

    @staticmethod
    def non_active_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.USER_RESOURCE.value})
        UserRepository.non_active_user(user)
        return None


    @staticmethod
    def get_latest_nip():
        return DataKaryawanRepository.get_latest_nip()

    @staticmethod
    def get_posible_pic(jabatan_id):
        return UserRepository.get_posible_pic(jabatan_id)

    @staticmethod
    def change_password(user, password):
        UserRepository.change_password(user, password)

    @staticmethod
    def resend_login_data(user_id):
        print(f"user_id: {user_id}")
        user = UserRepository.get_user_by_id(user_id)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.USER_RESOURCE.value})

        password = generate_password()

        UserService.change_password(user, password)

        try:
            NotificationService.send_notification_login_data(
                phone=user.phone,
                username=user.username,
                password=password,
                fullname=user.fullname,
                nip=user.data_karyawan.nip
            )
        except Exception as e:
            print(f"Sending notification failed: {str(e)}")
