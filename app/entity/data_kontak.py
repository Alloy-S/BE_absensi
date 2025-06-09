from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DataKontak(db.Model):
    __tablename__ = 'data_kontak'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alamat = db.Column(db.String(255), nullable=False)
    no_telepon = db.Column(db.String(20), nullable=True)
    nama_darurat = db.Column(db.String(150), nullable=True)
    no_telepon_darurat = db.Column(db.String(20), nullable=True)
    relasi_darurat = db.Column(db.String(50), nullable=True)
    
    user = db.relationship('Users', back_populates='data_kontak')
    
    def __repr__(self):
        return f"<DataKontak(id={self.id}, alamat='{self.alamat}', kota_kabupaten='{self.kota_kabupaten}', provinsi='{self.provinsi}')>"