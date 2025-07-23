from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Photo(db.Model):
    __tablename__ = 'photo'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = db.Column(db.String(20), nullable=False)
    path =  db.Column(db.String(1000), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    mimetype = db.Column(db.String(255), nullable=False)
    
    reimburse = db.relationship("Reimburse", back_populates="photo")
    
    def __repr__(self):
        return f"<Photo(id={self.id}, type='{self.type}', path='{self.path}')>"