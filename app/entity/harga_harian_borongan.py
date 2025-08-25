from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class HargaHarianBorongan(db.Model):
    __tablename__ = 'harga_harian_borongan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(100), nullable=False)
    harga_normal = db.Column(db.Numeric(12,2), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    detail_absensi_borongan = db.relationship("DetailAbsensiBorongan", back_populates="harga", lazy="joined")
    
    def __repr__(self):
        return (f"<HargaHarianBorongan(id={self.id}, nama='{self.nama}', harga_normal={self.harga_normal}')>")
    
    
    