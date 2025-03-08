from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ApprovalKehadiran(db.Model):
    __tablename__ = 'approval_kehadiran'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())  
    status = db.Column(db.String(10), nullable=False)
    approval_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    absensi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('absensi.id'), nullable=False)
    
    user = db.relationship("Users", back_populates="approval_kehadiran")
    absensi = db.relationship("Absensi", back_populates="approval_kehadiran")
    
    def __repr__(self):
        return (
            f"<ApprovalKehadiran(id={self.id}, date='{self.date}', status='{self.status}', "
            f"approval_user_id={self.approval_user_id}, absensi_id={self.absensi_id})>"
        )