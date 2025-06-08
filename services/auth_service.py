from repositories.user_repository import UserRepository

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        user = UserRepository.get_user_by_username(username)
        if user and user.check_password(password):
            return user
        return None