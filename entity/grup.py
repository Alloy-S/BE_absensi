from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Grup(db.Model):
    __tablename__ = 'grup'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(50), nullable=False)  
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="grup")
    
    def __repr__(self):
        return f"Grup('{self.nama}')"