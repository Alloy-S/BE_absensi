from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Lembur(db.Model):
    __tablename__ = 'lembur'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False)
    time_start = db.Column(db.Time, nullable=False)
    time_end = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('Users', back_populates="lembur")
    approval_lembur = db.relationship("ApprovalLembur", back_populates="lembur")
    
    def __repr__(self):
        return f"<Lembur(id={self.id}, user_id={self.user_id}, date={self.date}, start={self.time_start}, end={self.time_end}, status={self.status})>"