from app.database import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class ReminderLog(db.Model):
    __tablename__ = 'reminder_log'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, index=True)
    reminder_type = db.Column(db.String(20), nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date = db.Column(db.Date, nullable=False, index=True)

    user = db.relationship("Users", back_populates="reminder_log", lazy="select")