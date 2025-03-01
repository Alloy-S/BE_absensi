from repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_all_users():
        return UserRepository.get_all_users()

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def create_user(name, email, password):
        return UserRepository.create_user(name, email, password)

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
