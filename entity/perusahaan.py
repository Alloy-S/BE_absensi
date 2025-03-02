from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Perusahaan(db.Model):
    __tablename__ = 'perusahaan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alamat = db.Column(db.String(255), nullable=False)
    kota_kabupaten = db.Column(db.String(100), nullable=False)
    provinsi = db.Column(db.String(100), nullable=False)
    negara = db.Column(db.String(50), nullable=True)
    no_telepon = db.Column(db.String(20), nullable=True)
    kode_pos = db.Column(db.String(10), nullable=True)
    
    def __repr__(self):
        return f"<Perusahaan(id={self.id}, alamat='{self.alamat}', kota_kabupaten='{self.kota_kabupaten}', provinsi='{self.provinsi}', negara='{self.negara}', no_telepon='{self.no_telepon}', kode_pos='{self.kode_pos}')>"
    
    