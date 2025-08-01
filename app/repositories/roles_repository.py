from app.database import db
from app.entity import Roles

class RolesRepository:

    @staticmethod
    def get_all_roles():
        return Roles.query.all()


    @staticmethod
    def get_roles_by_role_ids(roles_ids):
        return db.session.query(Roles).filter(Roles.id.in_(roles_ids)).all()