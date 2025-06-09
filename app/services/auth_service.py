from app.execption.custom_execption import GeneralException
from app.repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token

from app.utils.error_code import ErrorCode


class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        user = UserRepository.get_user_by_username(username)
        if user and user.check_password(password):
            access_token = create_access_token(
                identity=user.username,
                additional_claims={
                    'name': user.fullname,
                    'role': user.user_role.name
                },
                expires_delta=False
            )

            response = {
                'token': access_token,
                'username': user.username,
                'fullname': user.fullname,
                'role': user.user_role.name
            }
            return response
        raise GeneralException(ErrorCode.INCORRECT_PASSWORD_OR_USERNAME)