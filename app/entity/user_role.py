from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserRole(db.Model):
    __tablename__ = 'user_role'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(256), nullable=False)
    kode = db.Column(db.Integer, nullable=True)
    
    users =  db.relationship('Users', back_populates='user_role')
    
    def __repr__(self):
        return f"UserRole('{self.name}')"