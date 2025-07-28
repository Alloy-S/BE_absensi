from app.repositories.user_repository import UserRepository
from app.repositories.dashboard_user_repository import DashboardUserRepository
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam

class DashboardUserService:

    @staticmethod
    def get_waiting_for_approvals_user(username):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        result = DashboardUserRepository.get_all_approval_status_waiting(user.id)

        response = {
            "approvals": result
        }

        return response
