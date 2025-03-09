from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class JadwalKerja(db.Model):
    __tablename__ = 'jadwal_kerja'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shift = db.Column(db.String(50), nullable=False)  
    time_in = db.Column(db.Time, nullable=False)  
    time_out = db.Column(db.Time, nullable=False)  
    toler_in = db.Column(db.SmallInteger , nullable=False)  
    toler_out = db.Column(db.SmallInteger , nullable=False)
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="jadwal_kerja")
    
    def __repr__(self):
        return f"<JadwalKerja(id={self.id}, shift='{self.shift}', time_in='{self.time_in}', time_out='{self.time_out}', toler_in={self.toler_in}, toler_out={self.toler_out})>"