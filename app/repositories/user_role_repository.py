from app.database import db
from app.entity import UserRole

class UserRoleRepository:

    @staticmethod
    def get_user_role(user_id):
        return db.session.query(UserRole).filter(UserRole.user_id == user_id).all()


    @staticmethod
    def update_user_role(user, new_roles):
        user_role_to_del = db.session.query(UserRole).filter(UserRole.user_id == user.id).all()

        for old_role in user_role_to_del:
            db.session.delete(old_role)

        for role in new_roles:
            new_user_role = UserRole(
                user_id=user.id,
                role_id=role.id,
            )
            db.session.add(new_user_role)



