from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class GrupGaji(db.Model):
    __tablename__ = 'grup_gaji'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grup_kode = db.Column(db.String(5), unique=True, nullable=False)
    grup_name = db.Column(db.String(100), nullable=False)
    
    grup_gaji_kom = db.relationship('GrupGajiKom', back_populates='grup_gaji')
    data_karyawan = db.relationship('DataKaryawan', back_populates='grup_gaji')
    
    def __repr__(self):
        return f"<GrupGaji(key='{self.grup_kode}', value='{self.grup_name}')>"