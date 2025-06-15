from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ApprovalIzin(db.Model):
    __tablename__ = 'approval_izin'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(30), nullable=False)
    approval_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    izin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('izin.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    approval_user = db.relationship("Users", back_populates="approval_user_izin", foreign_keys=[approval_user_id])
    user = db.relationship("Users", back_populates="approval_izin", foreign_keys=[user_id])
    izin = db.relationship("Izin", back_populates="approval_izin")
    
    def __repr__(self):
        return (
            f"<ApprovalIzin(id={self.id}, created_date='{self.created_date}', status='{self.status}', "
            f"approval_user_id={self.approval_user_id}, izin_id={self.izin_id}, user_id={self.user_id})>"
        )