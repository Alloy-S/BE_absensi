from email.policy import default

from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JadwalKerja(db.Model):
    __tablename__ = 'jadwal_kerja'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kode = db.Column(db.String(5), nullable=False)  
    shift = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, server_default='true', nullable=False, index=True)
    parent_schedule_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jadwal_kerja.id'), nullable=True)
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="jadwal_kerja")
    detail_jadwal_kerja = db.relationship('DetailJadwalKerja', back_populates='jadwal_kerja')
    absensi = db.relationship("Absensi", back_populates="jadwal_kerja")
    
    
    def __repr__(self):
        return f"<JadwalKerja(id={self.id}, kode='{self.kode}', shift='{self.shift}')>"