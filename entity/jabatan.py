from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Jabatan(db.Model):
    __tablename__ = 'jabatan'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama = db.Column(db.String(50), nullable=False)  
    parent_id = db.Column(UUID(as_uuid=True), db.ForeignKey('jabatan.id'), nullable=True)
    
    data_karyawan = db.relationship("DataKaryawan", back_populates="jabatan")
    # Self-referential relationship
    children = db.relationship(
        "Jabatan",
        backref=db.backref('parent', remote_side=[id])
    )
    
    def __repr__(self):
        return f"Jabatan('{self.nama}')"