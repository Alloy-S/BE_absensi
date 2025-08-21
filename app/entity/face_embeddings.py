from sqlalchemy.dialects.postgresql import ARRAY, UUID
from app.database import db
import uuid

class FaceEmbeddings(db.Model):
    __tablename__ = 'face_embeddings'
    
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    embedding_data = db.Column(db.Text, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("Users", back_populates="face_embeddings", uselist=False)

    def __repr__(self):
        return f"<FaceEmbeddings(id={self.id}, user_id={self.user_id})>"