from app.database import db
from app.repositories.roles_repository import RolesRepository
from app.repositories.user_repository import UserRepository
from app.services.notification_service import NotificationService
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
from app.utils.global_utils import format_string
from app.repositories.user_role_repository import UserRoleRepository

class RoleManagementService:

    @staticmethod
    def get_user_role_by_user_id(user_id):
        return UserRoleRepository.get_user_role(user_id)

    @staticmethod
    def get_all_roles():
        return RolesRepository.get_all_roles()

    @staticmethod
    def update_user_role(user_id, request):

        user = UserRepository.get_user_by_id(user_id)

        if not user:
            GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resouce': AppConstants.USER_RESOURCE.value})

        role_ids = request.get('role_ids', [])

        if len(role_ids) == 0:
            raise GeneralException(ErrorCode.USER_ROLE_EMPTY)

        new_roles = RolesRepository.get_roles_by_role_ids(role_ids)

        UserRoleRepository.update_user_role(user, new_roles)

        db.session.commit()

        NotificationService.send_notification_logout(user.fcm_token)

