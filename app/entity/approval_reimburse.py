from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ApprovalReimburse(db.Model):
    __tablename__ = 'approval_reimburse'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(30), nullable=False)
    approval_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    reimburse_id = db.Column(UUID(as_uuid=True), db.ForeignKey('reimburse.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    approval_user = db.relationship("Users", back_populates="approval_user_reimburse", foreign_keys=[approval_user_id])
    user = db.relationship("Users", back_populates="approval_reimburse", foreign_keys=[user_id])
    reimburse = db.relationship("Reimburse", back_populates="approval_reimburse")
    
    def __repr__(self):
        return (
            f"<ApprovalReimburse(id={self.id}, date='{self.date}', status='{self.status}', "
            f"approval_user_id={self.approval_user_id}, reimburse_id={self.reimburse_id})>"
        )
    
    