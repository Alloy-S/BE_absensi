from deepface import DeepFace
from scipy.spatial.distance import cosine
from app.entity import Users, FaceEmbeddings

from app.repositories.user_repository import UserRepository
from app.repositories.face_embeddings_repository import FaceEmbeddingsRepository

MODEL_NAME = 'SFace'
VERIFICATION_THRESHOLD = 0.593
DETECTOR_BACKEND = 'opencv'

class FaceRecognitionService:

    @staticmethod
    def _generate_embedding(image_path: str) -> list:
        try:
            embedding_objs = DeepFace.represent(
                img_path=image_path,
                model_name=MODEL_NAME,
                enforce_detection=True,
                detector_backend=DETECTOR_BACKEND
            )

            print(f"{len(embedding_objs)} embeddings found.")

            if len(embedding_objs) > 1:
                raise ValueError(
                    "Lebih dari satu wajah terdeteksi di dalam gambar. Harap gunakan gambar dengan satu wajah.")

            return embedding_objs[0]['embedding']

        except ValueError as e:
            raise ValueError(f"Analisis wajah gagal: {str(e)}")

    @staticmethod
    def register_face(user_id: str, image_path: str) -> FaceEmbeddings:
        existing_embedding = FaceEmbeddingsRepository.get_face_embeddings(user_id)
        if existing_embedding:
            raise ValueError(f"Pengguna dengan ID {user_id} sudah memiliki wajah terdaftar.")

        embedding_list = FaceRecognitionService._generate_embedding(image_path)

        new_face_embedding = FaceEmbeddingsRepository.save_face_embeddings(user_id, embedding_list)

        user = UserRepository.get_user_by_id(user_id)

        UserRepository.mark_done_register_face(user)

        return new_face_embedding

    @staticmethod
    def verify_face(user_id: str, image_path: str) -> bool:
        stored_embedding_obj = FaceEmbeddings.query.filter_by(user_id=user_id).first()
        if not stored_embedding_obj:
            raise ValueError("Tidak ada wajah terdaftar untuk pengguna ini.")

        stored_embedding = stored_embedding_obj.embedding

        new_embedding = FaceRecognitionService._generate_embedding(image_path)

        distance = cosine(stored_embedding, new_embedding)

        print(f"{user_id}: {distance}")
        return distance <= VERIFICATION_THRESHOLD
