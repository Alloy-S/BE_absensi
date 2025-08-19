from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Lembur(db.Model):
    __tablename__ = 'lembur'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    keterangan = db.Column(db.Text, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('Users', back_populates="lembur")
    approval_lembur = db.relationship("ApprovalLembur", back_populates="lembur", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Lembur(id={self.id}, user_id={self.user_id}, date={self.date}, date_start={self.date_start}, date_end={self.date_end}, status={self.status})>"