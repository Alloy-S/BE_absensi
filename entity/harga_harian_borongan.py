from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class HargaHarianBorongan(db.Model):
    __tablename__ = 'harga_harian_borongan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(100), nullable=False)
    harga_normal = db.Column(db.Numeric(9,2), nullable=False)
    harga_lembur = db.Column(db.Numeric(9,2), nullable=False, default=0)
    jam_start_normal = db.Column(db.Time, nullable=False)
    jam_end_normal = db.Column(db.Time, nullable=False)
    toleransi_waktu = db.Column(db.SmallInteger, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    
    absensi_borongan = db.relationship("AbsensiBorongan", back_populates="harga")
    
    def __repr__(self):
        return (f"<HargaHarianBorongan(id={self.id}, nama='{self.nama}', harga_normal={self.harga_normal}, "
                f"harga_lembur={self.harga_lembur}, jam_start_normal={self.jam_start_normal}, "
                f"jam_end_normal={self.jam_end_normal}, toleransi_waktu={self.toleransi_waktu}, date='{self.date}')>")
    
    
    