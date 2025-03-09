from entity.users import Users
from database import db

class UserRepository:
    @staticmethod
    def get_all_users():
        return Users.query.all()

    @staticmethod
    def get_user_by_id(user_id):
        return Users.query.filter_by(id=user_id).first()
    
    @staticmethod
    def get_user_by_username(username):
        return Users.query.filter_by(username=username).first()

    @staticmethod
    def create_user(name, username, password):
        new_user = Users(name=name, username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def update_user(user, name, email):
        user.name = name
        user.email = email
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user):
        db.session.delete(user)
        db.session.commit()
