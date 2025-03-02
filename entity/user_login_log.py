from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class UserLoginLog(db.Model):
    __tablename__ = 'user_login_log'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_time = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    status = db.Column(db.String(10), nullable=False) 
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    users = db.relationship("Users", back_populates="login_log")  
    
    def __repr__(self):
        return f"<UserLoginLog(date_time='{self.date_time}', status='{self.status}', user_id='{self.user_id}')>"