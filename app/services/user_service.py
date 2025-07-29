from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.data_kontak_repository import DataKontakRepository
from app.repositories.data_pribadi_repository import DataPribadiRepository
from app.repositories.jabatan_repository import JabatanRepository
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
    def get_users_pagination_kuota_cuti(page, per_page, search):
        return UserRepository.get_users_pagination_kuota_cuti(page=page, per_page=per_page, search=search)

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

        jabatan = JabatanRepository.get_by_id(data_karyawan.get('jabatan_id'))

        if not jabatan:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.JABATAN_RESOURCE.value})

        user_pic_id = data_karyawan.get('user_pic_id')

        print("pic: " + user_pic_id)

        if jabatan.parent_id is not None:
            if not user_pic_id:
                raise GeneralException(ErrorCode.MANDATORY_PIC)

        else:
            if user_pic_id:
                raise GeneralException(ErrorCode.HIGHEST_POSITION)

            data_karyawan['user_pic_id'] = None

        result = UserRepository.create_user(fullname, username, password, data_pribadi, data_kontak, data_karyawan, nip)

        try:
            NotificationService.send_notification_login_data(phone=result.phone, username=username, password=password, fullname=fullname, nip=nip)
        except Exception as e:
            print(f"Sending notification failed: {str(e)}")

        return None

    @staticmethod
    def create_user_admin():

        username = "00000000"
        password = "superadmin"
        fullname = "SUPERADMIN"
        phone = "089686757322"

        UserRepository.create_user_admin(fullname, username, password, phone)

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
    def change_password(username, validated):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        if validated['new_pass'] != validated['verify_pass']:
            raise GeneralException(ErrorCode.NEW_PASSWORD_NOT_MATCH)

        if not user.check_password(validated['old_pass']):
            raise GeneralException(ErrorCode.INCORRECT_PASSWORD)

        UserRepository.change_password(user, validated['new_pass'])


    @staticmethod
    def resend_login_data(user_id):
        print(f"user_id: {user_id}")
        user = UserRepository.get_user_by_id(user_id)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.USER_RESOURCE.value})

        password = generate_password()

        UserRepository.change_password(user, password)

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

    @staticmethod
    def get_data_karyawan(username):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        data_karyawan = DataKaryawanRepository.get_data_karyawan_by_user_id(user.id)

        if not data_karyawan:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.DATA_KARYAWAN_RESOURCE.value})

        return data_karyawan

    @staticmethod
    def get_data_kontak(username):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        kontak = DataKontakRepository.get_data_kontak_by_user_id(user.id)

        if not kontak:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.DATA_KONTAK_RESOURCE.value})

        return kontak

    @staticmethod
    def get_data_pribadi(username):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        data_pribadi = DataPribadiRepository.get_data_pribadi_by_user_id(user.id)

        if not data_pribadi:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.DATA_PRIBADI_RESOURCE.value})

        return data_pribadi


    @staticmethod
    def edit_data_pribadi(username, validated):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        UserRepository.edit_data_pribadi(user, validated)

    @staticmethod
    def edit_data_kontak(username, validated):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        UserRepository.edit_data_kontak(user, validated)

    @staticmethod
    def get_users_by_pic_id(username):
        user_pic = UserRepository.get_user_by_username(username)
        if not user_pic:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        return UserRepository.get_users_by_pic(user_pic.id)

    @staticmethod
    def update_fcm_token_user(username, request):
        user = UserRepository.get_user_by_username(username)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        UserRepository.update_fcm_token(user, request.get('fcm_token'))

