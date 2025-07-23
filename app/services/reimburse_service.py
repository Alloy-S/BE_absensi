from app.repositories.approval_reimburse_repository import ApprovalReimburseRepository
from app.repositories.detail_reimburse_repository import DetailReimburseRepository
from app.repositories.user_repository import UserRepository
from app.repositories.reimburse_repository import ReimburseRepository
from app.repositories.photo_repository import PhotoRepository
from app.services.photo_service import PhotoService
from app.database import db
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam


class ReimburseService:

    @staticmethod
    def create_approval_reimburse(username, data):
        try:
            user = UserRepository.get_user_by_username(username)

            if not user:
                raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                                params={'resource': AppConstants.USER_RESOURCE.value})

            photo = PhotoService.save_photo(data['photo'])

            reimburse = ReimburseRepository.create_reimburse({
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'photo_id': photo.id,
                'created_by': user.id
            })

            detail_reimburse = data['details']

            for item in detail_reimburse:
                DetailReimburseRepository.create_detail_reimburse({
                    'nama': item['nama'],
                    'harga': item['harga'],
                    'jumlah': item['jumlah'],
                    'reimburse_id': reimburse.id
                })

            new_approval = ApprovalReimburseRepository.create_approval_reimburse({
                'status': AppConstants.WAITING_FOR_APPROVAL.value,
                'approval_user_id': user.data_karyawan.user_pic_id,
                'reimburse_id': reimburse.id,
            }, user.id)

            db.session.commit()

            return new_approval

        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def get_approval_reimburse_by_id(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        approval = ApprovalReimburseRepository.get_approval_by_id(approval_id, user.id)

        if not approval:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.APPROVAL_REIMBURSE_RESOURCE.value})

        return approval

    @staticmethod
    def get_approval_reimburse_pagination(username, request):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})

        return ApprovalReimburseRepository.get_approval_pagination(user.id, request['filter_status'], request['page'], request['size'])

    @staticmethod
    def get_approval_by_pic_id(pic_username, request):

        user = UserRepository.get_user_by_username(pic_username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})
        return ApprovalReimburseRepository.get_approval_pagination_by_pic(user.id, request['filter_status'], request['page'], request['size'])

    @staticmethod
    def cancel_approval_reimburse(username, approval_id):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.APPROVAL_ABSENSI_BORONGAN_RESOURCE.value})


        approval = ApprovalReimburseRepository.get_approval_by_id(approval_id, user.id)




        ApprovalReimburseRepository.delete_approval_reimburse(approval.id)
        DetailReimburseRepository.delete_detail_reimburse(approval.reimburse.id)
        ReimburseRepository.delete_reimburse(approval.reimburse.id)

        PhotoService.delete_photo(approval.reimburse.photo_id)

        db.session.commit()


