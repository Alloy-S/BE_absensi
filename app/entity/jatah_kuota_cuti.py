from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JatahKuotaCuti(db.Model):
    __tablename__ = 'jatah_kuota_cuti'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    year = db.Column(db.SmallInteger, nullable=False)
    kuota = db.Column(db.Integer, nullable=False)
    izin_digunakan = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    jenis_izin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jenis_izin.id'), nullable=False)
    
    user = db.relationship("Users", back_populates="jatah_kuota_cuti")
    jenis_izin = db.relationship("JenisIzin", back_populates="jatah_kuota_cuti")