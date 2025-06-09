from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class KuotaCuti(db.Model):
    __tablename__ = 'kuota_cuti'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(256), nullable=False)
    
    jatah_kuota_cuti = db.relationship("JatahKuotaCuti", back_populates="kuota_cuti")