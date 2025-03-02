from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Izin(db.Model):
    __tablename__ = 'izin'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    tgl_izin = db.Column(db.Date, nullable=False)
    keterangan = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(10), nullable=False)
    jenis_izin_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jenis_izin.id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    
    jenis_izin = db.relationship("JenisIzin", back_populates="izin")
    user = db.relationship("Users", back_populates='izin')
    approval_izin = db.relationship("ApprovalIzin", back_populates="izin")
    
    def __repr__(self):
        return (f"<Izin(id={self.id}, date='{self.date}', tgl_izin='{self.tgl_izin}', status='{self.status}', "
                f"jenis_izin_id={self.jenis_izin_id}, user_id={self.user_id})>")
    
    