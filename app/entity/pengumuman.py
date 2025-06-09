from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Pengumuman(db.Model):
    __tablename__ = 'pengumuman'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    judul = db.Column(db.String(50), nullable=False)
    isi = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    created_by = db.Column(db.String(50), nullable=False)
    
    def __repr__(self):
        return f"<Pengumuman(id={self.id}, judul={self.judul}, is_active={self.is_active}, date_created={self.date_created})>"