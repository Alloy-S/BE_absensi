from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserRole(db.Model):
    __tablename__ = 'user_role'
    
    user_id = db.Column(UUID, db.ForeignKey('users.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True)
    
    users =  db.relationship('Users', back_populates='user_role')
    role = db.relationship('Roles', back_populates='user_role')
    
    def __repr__(self):
        return f"UserRole('{self.name}')"