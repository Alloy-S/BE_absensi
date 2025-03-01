from repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def authenticate_user(email, password):
        user = UserRepository.get_user_by_email(email)
        if user and user.check_password(password):
            return user
        return None