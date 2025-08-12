from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLAEnum
from app.enums.hitung_kom_gaji import HitungKomGaji

class GrupGajiKom(db.Model):
    __tablename__ = 'grup_gaji_kom'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    use_kondisi = db.Column(db.Boolean, nullable=False)
    kode_kondisi = db.Column(db.String(50), nullable=False)
    min_kondisi = db.Column(db.SmallInteger, nullable=False)
    max_kondisi = db.Column(db.SmallInteger, nullable=False)
    use_formula = db.Column(db.Boolean, nullable=False)
    kode_formula = db.Column(db.String(50), nullable=False)
    operation_sum = db.Column(db.String(1), nullable=False)
    nilai_uang = db.Column(db.Numeric(9,2), nullable=False)
    hitung = db.Column(SQLAEnum(HitungKomGaji, name="hitung"), nullable=False)
    
    grp_id = db.Column(UUID(as_uuid=True), db.ForeignKey('grup_gaji.id'), nullable=False)
    kom_id = db.Column(UUID(as_uuid=True), db.ForeignKey('komponen_gaji.id'), nullable=False)
    
    grup_gaji = db.relationship('GrupGaji', back_populates='grup_gaji_kom')
    komponen_gaji = db.relationship('KomponenGaji', back_populates='grup_gaji_kom')
    
    def __repr__(self):
        return f"<GrupGajiKom(key='{self.grup_kode}', value='{self.grup_name}')>"