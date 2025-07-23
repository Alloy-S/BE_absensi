from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DataPribadi(db.Model):
    __tablename__ = 'data_pribadi'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    gender = db.Column(db.String(10), nullable=False)  
    tgl_lahir = db.Column(db.Date, nullable=False)  
    tmpt_lahir = db.Column(db.String(150), nullable=True)
    status_kawin = db.Column(db.String(20), nullable=True) 
    agama = db.Column(db.String(30), nullable=True)  
    gol_darah = db.Column(db.String(3), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, unique=True)
    
    user = db.relationship('Users', back_populates='data_pribadi')

    def __repr__(self):
        return f"<DataPribadi(id={self.id}, gender='{self.gender}', tgl_lahir='{self.tgl_lahir}', user_id='{self.user_id}')>"
