from database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class ConfigProps(db.Model):
    __tablename__ = 'config_props'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(256), nullable=False)
    
    def __repr__(self):
        return f"<ConfigProps(key='{self.key}', value='{self.value}')>"