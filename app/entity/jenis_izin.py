from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JenisIzin(db.Model):
    __tablename__ = 'jenis_izin'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(100), nullable=False)
    default_kuota = db.Column(db.Integer, nullable=False)
    
    izin = db.relationship('Izin', back_populates='jenis_izin')
    jatah_kuota_cuti = db.relationship("JatahKuotaCuti", back_populates="jenis_izin")
    
    def __repr__(self):
        return f"<JenisIzin(nama='{self.nama}')>"