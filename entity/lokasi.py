from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Lokasi(db.Model):
    __tablename__ = 'lokasi'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(50), nullable=False) 
    latitude = db.Column(db.Numeric(9, 6), nullable=False)
    longitude = db.Column(db.Numeric(9, 6), nullable=False)
    toleransi = db.Column(db.SmallInteger, nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="lokasi")
    
    def __repr__(self):
        return f"<Lokasi(id={self.id}, name='{self.nama}', latitude={self.latitude}, longitude={self.longitude})>"