from app.database import db
from sqlalchemy.dialects.postgresql import UUID

class RolePermissions(db.Model):
    __tablename__ = 'role_permissions'

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    permission_id = db.Column(db.Integer, db.ForeignKey('permission.id'), primary_key=True)

    role = db.relationship('Roles', back_populates='role_permission', lazy="joined")
    permission = db.relationship('Permission', back_populates='role_permission', lazy="joined")

    def __repr__(self):
        return f"<RolePermissions(role_permission_id='{self.user_role_id}', permission_id='{self.permission_id}')>"