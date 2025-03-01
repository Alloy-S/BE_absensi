from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class DataKontak(db.Model):
    __tablename__ = 'data_kontak'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)