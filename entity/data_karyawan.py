from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DataKaryawan(db.Model):
    __tablename__ = 'data_karyawan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nip = db.Column(db.String(18), nullable=False) 
    tgl_gabung = db.Column(db.Date, nullable=False)  
    lokasi_kerja = db.Column(db.String(150), nullable=False)
    tipe_karyawan = db.Column(db.String(30), nullable=True) 
    jabatan = db.Column(db.String(50), nullable=True) 
    
    user = db.relationship('Users', back_populates='data_karyawan')

    def __repr__(self):
        return (f"<DataKaryawan(id={self.id}, nip='{self.nip}', tgl_gabung='{self.tgl_gabung}', "
                f"lokasi_kerja='{self.lokasi_kerja}', tipe_karyawan='{self.tipe_karyawan}', "
                f"jabatan='{self.jabatan}')>")