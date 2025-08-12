from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLAEnum
from app.enums.tipe_kom_gaji import TipeKomGaji
from app.enums.hitung_kom_gaji import HitungKomGaji

class KomponenGaji(db.Model):
    __tablename__ = 'komponen_gaji'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    kom_kode = db.Column(db.String(10), nullable=False)
    kom_name = db.Column(db.String(100), nullable=False) 
    no_urut = db.Column(db.SmallInteger, nullable=False) 
    tipe = db.Column(SQLAEnum(TipeKomGaji, name="tipe_kom_gaji"), nullable=False)
    hitung = db.Column(SQLAEnum(HitungKomGaji, name="hitung_kom_gaji"), nullable=False)
    
    grup_gaji_kom = db.relationship('GrupGajiKom', back_populates='komponen_gaji')
    
    
    def __repr__(self):
        return (
            f"<KomponenGaji("
            f"id={self.id}, "
            f"kom_kode='{self.kom_kode}', "
            f"kom_name='{self.kom_name}', "
            f"no_urut={self.no_urut}, "
            f"tipe='{self.tipe.value}', "
            f"hitung='{self.hitung.value}'"
            f")>"
        )
