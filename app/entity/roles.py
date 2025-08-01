from app.database import db


class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    role_permission = db.relationship('RolePermissions', back_populates='role')
    user_role = db.relationship('UserRole', back_populates='role')

    def __repr__(self):
        return f"<Roles(id='{self.id}', name='{self.name}')>"