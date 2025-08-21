from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DataKontak(db.Model):
    __tablename__ = 'data_kontak'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    alamat = db.Column(db.Text, nullable=False)
    no_telepon = db.Column(db.Text, nullable=True)
    nama_darurat = db.Column(db.String(150), nullable=True)
    no_telepon_darurat = db.Column(db.Text, nullable=True)
    relasi_darurat = db.Column(db.String(50), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, unique=True)
    
    user = db.relationship('Users', back_populates='data_kontak')
    
    def __repr__(self):
        return f"<DataKontak(id={self.id}, user_id='{self.user_id}')>"