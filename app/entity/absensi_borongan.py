from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class AbsensiBorongan(db.Model):
    __tablename__ = 'absensi_borongan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ton_normal = db.Column(db.Numeric(9,2), nullable=False)
    ton_lembur = db.Column(db.Numeric(9,2), nullable=False, default=0)
    tipe = db.Column(db.String(20), nullable=False)
    total = db.Column(db.Numeric(9,2), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    harga_id = db.Column(UUID(as_uuid=True), db.ForeignKey('harga_harian_borongan.id'), nullable=False)
    
    harga = db.relationship("HargaHarianBorongan", back_populates="absensi_borongan", lazy="joined")
    
    def __repr__(self):
        return (f"<AbsensiBorongan(id={self.id}, ton_normal={self.ton_normal}, ton_lembur={self.ton_lembur}, "
                f"tipe='{self.tipe}', total={self.total}, date='{self.date}', harga_id={self.harga_id})>")