from app.database import db
from app.entity.face_embeddings import FaceEmbeddings

class FaceEmbeddingsRepository:

    @staticmethod
    def get_face_embeddings(user_id):
        return FaceEmbeddings.query.filter_by(user_id=user_id).first()

    @staticmethod
    def save_face_embeddings(user_id, embedding):
        new_face_embedding = FaceEmbeddings(user_id=user_id, embedding=embedding)

        db.session.add(new_face_embedding)
        db.session.commit()

        return new_face_embedding