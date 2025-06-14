from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JatahKuotaCuti(db.Model):
    __tablename__ = 'jatah_kuota_cuti'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(256), nullable=False)
    data_karyawan_id = db.Column(UUID(as_uuid=True), db.ForeignKey('data_karyawan.id'), nullable=False)
    kuota_cuti_id = db.Column(UUID(as_uuid=True), db.ForeignKey('kuota_cuti.id'), nullable=False)
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="jatah_kuota_cuti")
    kuota_cuti = db.relationship("KuotaCuti", back_populates="jatah_kuota_cuti")