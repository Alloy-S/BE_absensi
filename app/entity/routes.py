from app.database import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Route(db.Model):
    __tablename__ = 'routes'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    path = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    component = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)
    parent = db.Column(db.String, nullable=True)
    meta = db.Column(db.JSON, nullable=True)
    order = db.Column(db.Integer, nullable=True)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Route(name='{self.name}', path='{self.path}')>"