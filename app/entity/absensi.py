from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Absensi(db.Model):
    __tablename__ = 'absensi'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    lokasi = db.Column(db.String(50), nullable=False)
    metode = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('Users', back_populates="absensi")
    detail_absensi = db.relationship("DetailAbsensi", back_populates="absensi")
    approval = db.relationship("ApprovalKoreksi", back_populates="absensi")
    
    def __repr__(self):
        return (f"<Absensi(id={self.id}, date='{self.date}', lokasi='{self.lokasi}', metode='{self.metode}', "
                f"status='{self.status}', user_id={self.user_id})>")