from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Reimburse(db.Model):
    __tablename__ = 'reimburse'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    status = db.Column(db.String(30), nullable=False)
    photo_id = db.Column(UUID(as_uuid=True), db.ForeignKey('photo.id'), nullable=False)
    created_by = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    photo = db.relationship("Photo", back_populates="reimburse", uselist=False)
    user = db.relationship("Users", back_populates="reimburse")
    approval_reimburse = db.relationship("ApprovalReimburse", back_populates="reimburse")
    detail_reimburse = db.relationship("DetailReimburse", back_populates="reimburse")

    def __repr__(self):
        return (
            f"<Reimburse(id={self.id}, nama='{self.nama}', jumlah={self.jumlah}, "
            f"date='{self.date}', status='{self.status}', created_by={self.created_by})>"
        )
    