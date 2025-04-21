from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLAEnum
from enums.hari import Hari

class DetailJadwalKerja(db.Model):
    __tablename__ = 'detail_jadwal_kerja'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hari =  db.Column(SQLAEnum(Hari, name="hari"), nullable=False)
    time_in = db.Column(db.Time, nullable=False)
    time_out = db.Column(db.Time, nullable=False)
    toler_in = db.Column(db.SmallInteger , nullable=False)
    toler_out = db.Column(db.SmallInteger , nullable=False)
    
    
    jadwal_kerja_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jadwal_kerja.id'), nullable=False)
    
    jadwal_kerja = db.relationship('JadwalKerja', back_populates='detail_jadwal_kerja')
    
    
    def __repr__(self):
        return f"<DetailJadwalKerja(id={self.id}, jadwal_kerja_id='{self.jadwal_kerja_id}', time_in='{self.time_in}', time_out='{self.time_out}', toler_in={self.toler_in}, toler_out={self.toler_out})>"