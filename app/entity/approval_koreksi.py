from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ApprovalKoreksi(db.Model):
    __tablename__ = 'approval_koreksi'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    absensi_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), nullable=False)
    catatan_pengajuan = db.Column(db.Text, nullable=True)
    approval_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    absensi_id = db.Column(UUID(as_uuid=True), db.ForeignKey('absensi.id'), nullable=True)
    
    approval_user = db.relationship("Users", back_populates="approval_user_koreksi", foreign_keys=[approval_user_id])
    user = db.relationship("Users", back_populates="approval_koreksi", foreign_keys=[user_id])
    detail_approval = db.relationship("DetailApprovalKoreksi", back_populates="approval")
    absensi = db.relationship("Absensi", back_populates="approval")
    
    def __repr__(self):
        return (
            f"<ApprovalKoreksi(id={self.id}, date='{self.date}', status='{self.status}', "
            f"approval_user_id={self.approval_user_id}, detail_absensi_id={self.absensi_id})>"
        )