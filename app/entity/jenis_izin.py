from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JenisIzin(db.Model):
    __tablename__ = 'jenis_izin'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(100), nullable=False)
    kuota_default = db.Column(db.Integer, nullable=False, default=0)
    periode_reset = db.Column(db.String(50), nullable=False, default='TIDAK_ADA')
    berlaku_setelah_bulan = db.Column(db.Integer, nullable=False, default=0)
    
    izin = db.relationship('Izin', back_populates='jenis_izin')
    jatah_kuota_cuti = db.relationship("JatahKuotaCuti", back_populates="jenis_izin")
    
    def __repr__(self):
        return f"<JenisIzin(nama='{self.nama}')>"