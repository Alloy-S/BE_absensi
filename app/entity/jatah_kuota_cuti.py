from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JatahKuotaCuti(db.Model):
    __tablename__ = 'jatah_kuota_cuti'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    periode = db.Column(db.SmallInteger, nullable=False)
    kuota_awal = db.Column(db.Integer, nullable=False)
    kuota_terpakai = db.Column(db.Integer, nullable=False, default=0)
    sisa_kuota = db.Column(db.Integer, nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    jenis_izin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jenis_izin.id'), nullable=False)
    
    user = db.relationship("Users", back_populates="jatah_kuota_cuti")
    jenis_izin = db.relationship("JenisIzin", back_populates="jatah_kuota_cuti")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sisa_kuota = self.kuota_awal - self.kuota_terpakai