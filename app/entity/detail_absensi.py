from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DetailAbsensi(db.Model):
    __tablename__ = 'detail_absensi'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    type = db.Column(db.String(10), nullable=False)
    status_appv = db.Column(db.String(10), nullable=False)
    status_absensi = db.Column(db.String(10), nullable=False)
    latitude = db.Column(db.Numeric(9, 6), nullable=True)
    longitude = db.Column(db.Numeric(9, 6), nullable=True)
    id_absensi = db.Column(UUID(as_uuid=True), db.ForeignKey('absensi.id'), nullable=False)
    
    absensi = db.relationship("Absensi", back_populates="detail_absensi")
    approval_koreksi = db.relationship("ApprovalKoreksi", back_populates="detail_absensi")
    
    def __repr__(self):
        return (f"<DetailAbsensi(id={self.id}, date='{self.date}', type='{self.type}', status_appv='{self.status_appv}', "
                f"status_absensi='{self.status_absensi}', latitude={self.latitude}, longitude={self.longitude}, "
                f"id_absensi={self.id_absensi})>")