from app.execption.custom_execption import GeneralExceptionWithParam, GeneralException
from app.repositories.data_kontak_repository import DataKontakRepository
from app.repositories.data_pribadi_repository import DataPribadiRepository
from app.repositories.jabatan_repository import JabatanRepository
from app.repositories.user_repository import UserRepository
from app.services.encryption_service import EncryptionServiceAES256
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
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        decrypted_user_data = {
            'id': user.id,
            'fullname': user.fullname,
            'username': user.username,
            'phone': EncryptionServiceAES256.decrypt(user.phone),
            'user_role': user.user_role,
            'data_karyawan': None,
            'data_pribadi': None,
            'data_kontak': None,
        }

        if user.data_karyawan:
            decrypted_user_data['data_karyawan'] = {
                'id': user.data_karyawan.id,
                'nip': user.data_karyawan.nip,
                'tgl_gabung': user.data_karyawan.tgl_gabung,
                'tipe_karyawan': user.data_karyawan.tipe_karyawan,
                'jabatan': user.data_karyawan.jabatan,
                'jadwal_kerja': user.data_karyawan.jadwal_kerja,
                'lokasi': user.data_karyawan.lokasi,
                'pic': user.data_karyawan.pic,
                'user_pic_id': user.data_karyawan.user_pic_id,
                'grup_gaji_id': user.data_karyawan.grup_gaji_id,
                'gaji_pokok': user.data_karyawan.gaji_pokok,
                'face_recognition_mode': user.data_karyawan.face_recognition_mode,
            }

        if user.data_pribadi:
            decrypted_user_data['data_pribadi'] = {
                'id': user.data_pribadi.id,
                'gender': user.data_pribadi.gender,
                'tgl_lahir': EncryptionServiceAES256.decrypt(user.data_pribadi.tgl_lahir),
                'tmpt_lahir': user.data_pribadi.tmpt_lahir,
                'status_kawin': user.data_pribadi.status_kawin,
                'agama': user.data_pribadi.agama,
                'gol_darah': user.data_pribadi.gol_darah,
            }

        if user.data_kontak:
            decrypted_user_data['data_kontak'] = {
                'id': user.data_kontak.id,
                'alamat': EncryptionServiceAES256.decrypt(user.data_kontak.alamat),
                'no_telepon': EncryptionServiceAES256.decrypt(user.data_kontak.no_telepon),
                'nama_darurat': user.data_kontak.nama_darurat,
                'no_telepon_darurat': EncryptionServiceAES256.decrypt(user.data_kontak.no_telepon_darurat),
                'relasi_darurat': user.data_kontak.relasi_darurat,
            }

        return decrypted_user_data

    @staticmethod
    def get_user_by_username(username):
        return UserRepository.get_user_by_username(username)

    @staticmethod
    def create_user(fullname, data_pribadi, data_kontak, data_karyawan):

        if any(char.isalpha() for char in data_kontak['no_telepon']):
            raise GeneralException(ErrorCode.INVALID_PHONE_NUMBER_FORMAT)

        username = generate_username()
        password = generate_password()

        nip = DataKaryawanRepository.generate_new_nip()

        jabatan = JabatanRepository.get_by_id(data_karyawan.get('jabatan_id'))

        if not jabatan:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.JABATAN_RESOURCE.value})

        user_pic_id = data_karyawan.get('user_pic_id')

        if jabatan.parent_id is not None:
            if not user_pic_id:
                raise GeneralException(ErrorCode.MANDATORY_PIC)

        else:
            if user_pic_id:
                raise GeneralException(ErrorCode.HIGHEST_POSITION)

            data_karyawan['user_pic_id'] = None

        result = UserRepository.create_user(fullname, username, password, data_pribadi, data_kontak, data_karyawan, nip)

        if not data_karyawan['tipe_karyawan']:
            return

        try:
            NotificationService.send_notification_login_data(phone=data_kontak['no_telepon'], username=username, password=password,
                                                             fullname=fullname, nip=nip)
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
        if any(char.isalpha() for char in data['data_kontak']['no_telepon']):
            raise GeneralException(ErrorCode.INVALID_PHONE_NUMBER_FORMAT)

        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
        UserRepository.update_user(user, data)
        return None

    @staticmethod
    def non_active_user(user_id):
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})
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
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        password = generate_password()

        UserRepository.change_password(user, password)

        decrypted_phone = EncryptionServiceAES256.decrypt(user.phone)

        try:
            NotificationService.send_notification_login_data(
                phone=decrypted_phone,
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

        response = {
            'id': kontak.id,
            'alamat': EncryptionServiceAES256.decrypt(kontak.alamat),
            'no_telepon': EncryptionServiceAES256.decrypt(kontak.no_telepon),
            'nama_darurat': kontak.nama_darurat,
            'no_telepon_darurat': EncryptionServiceAES256.decrypt(kontak.no_telepon_darurat),
            'relasi_darurat': kontak.relasi_darurat,
        }

        return response

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


        response = {
            'id': data_pribadi.id,
            'gender': data_pribadi.gender,
            'tgl_lahir': EncryptionServiceAES256.decrypt(data_pribadi.tgl_lahir),
            'tmpt_lahir': data_pribadi.tmpt_lahir,
            'status_kawin': data_pribadi.status_kawin,
            'agama': data_pribadi.agama,
            'gol_darah': data_pribadi.gol_darah,
        }
        return response

    @staticmethod
    def edit_data_pribadi(username, validated):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        UserRepository.edit_data_pribadi(user, validated)

    @staticmethod
    def edit_data_kontak(username, validated):
        if any(char.isalpha() for char in validated['no_telepon']):
            raise GeneralException(ErrorCode.INVALID_PHONE_NUMBER_FORMAT)

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

    @staticmethod
    def get_waiting_by_approvals_user(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        response = UserRepository.get_all_approval_status_waiting(user.id, request.get('filter_tipe_approval'),
                                                                  request.get('page'), request.get('size'))

        return response

    @staticmethod
    def find_user_by_username_or_name(search):
        return UserRepository.find_user_by_username_or_name(search)
