from repositories.user_repository import UserRepository
from services.notification_service import NotificationService
from utils.global_utils import generate_password, generate_username
from repositories.data_karyawan_repository import DataKaryawanRepository


class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def create_user(fullname, data_pribadi, data_kontak, data_karyawan):

        username = generate_username()
        password = generate_password()

        nip = DataKaryawanRepository.generate_new_nip()

        result = UserRepository.create_user(fullname, username, password, data_pribadi, data_kontak, data_karyawan, nip)

        if not result:
            return None

        try:
            NotificationService.send_notification(phone=result.phone, username=username, password=password, fullname=fullname, nip=nip)
        except Exception as e:
            print(f"Sending notification failed: {str(e)}")
            return None

        return result

    @staticmethod
    def update_user(user_id, name, email):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None
        return UserRepository.update_user(user, name, email)

    @staticmethod
    def delete_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            return None
        UserRepository.delete_user(user)
        return True

    @staticmethod
    def get_latest_nip():
        return DataKaryawanRepository.get_latest_nip()
