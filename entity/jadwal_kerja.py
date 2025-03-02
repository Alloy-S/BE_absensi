from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JadwalKerja(db.Model):
    __tablename__ = 'jadwal_kerja'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shift = db.Column(db.String(50), nullable=False)  
    jam_in = db.Column(db.Time, nullable=False)  
    jam_out = db.Column(db.Time, nullable=False)  
    toler_in = db.Column(db.SmallInteger , nullable=False)  
    toler_out = db.Column(db.SmallInteger , nullable=False)  
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="jadwal_kerja")
    
    def __repr__(self):
        return f"<JadwalKerja(id={self.id}, shift='{self.shift}', jam_in='{self.jam_in}', jam_out='{self.jam_out}', toler_in={self.toler_in}, toler_out={self.toler_out})>"