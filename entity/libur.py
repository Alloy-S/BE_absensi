from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Libur(db.Model):
    __tablename__ = 'libur'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date = db.Column(db.Date, nullable=False)  
    is_holiday = db.Column(db.Boolean, nullable=False)