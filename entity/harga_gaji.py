from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class HargaGaji(db.Model):
    __tablename__ = 'harga_gaji'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(256), nullable=False)
    
    def __repr__(self):
        return f"<HargaGaji(key='{self.key}', value='{self.value}')>"