from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ApprovalLembur(db.Model):
    __tablename__ = 'approval_lembur'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(30), nullable=False)
    approval_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    lembur_id = db.Column(UUID(as_uuid=True), db.ForeignKey('lembur.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    approval_user = db.relationship("Users", back_populates="approval_user_lembur", foreign_keys=[approval_user_id])
    user = db.relationship("Users", back_populates="approval_lembur", foreign_keys=[user_id])
    lembur = db.relationship("Lembur", back_populates="approval_lembur")
    
    def __repr__(self):
        return (
            f"<ApprovalLembur(id={self.id}, created_date='{self.date}', status='{self.status}', "
            f"approval_user_id={self.approval_user_id}, lembur_id={self.lembur_id})>"
        )