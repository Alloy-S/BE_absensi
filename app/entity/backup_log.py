from app.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class BackupLog(db.Model):
    __tablename__ = 'backup_log'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='PENDING')
    filename = db.Column(db.String(255), nullable=True)
    file_path = db.Column(db.String(512), nullable=True)
    error_message = db.Column(db.Text, nullable=True)