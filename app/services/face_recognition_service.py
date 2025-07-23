import os
import base64
import uuid
from deepface import DeepFace
from scipy.spatial.distance import cosine
from app.entity import Users, FaceEmbeddings
from app.database import db
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam
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
                raise GeneralException(ErrorCode.FACE_MORE_THAN_ONE)

            return embedding_objs[0]['embedding']

        except ValueError as e:
            error_message = str(e)

            if os.path.exists(image_path):
                os.remove(image_path)

            if "Face could not be detected" in error_message:
                raise GeneralException(ErrorCode.FACE_NOT_FOUND)

            raise GeneralException(ErrorCode.FACE_DETECTION_FAILED)

    @staticmethod
    def get_face_registation_status(username):
        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        existing_embedding = FaceEmbeddingsRepository.get_face_embeddings(user.id)

        if not existing_embedding:
            status = False
        else:
            status = True

        return {
            'username': username,
            'face_registration_status': status
        }

    @staticmethod
    def register_face(username: str, request):
        base64_string = request['image']

        try:
            if "," in base64_string:
                _, base64_data = base64_string.split(",", 1)
            else:
                base64_data = base64_string

            image_data = base64.b64decode(base64_data)
        except (ValueError, TypeError):
            raise GeneralException(ErrorCode.INVALID_BASE64)

        filename = f"{uuid.uuid4()}.jpg"
        temp_path = os.path.join(AppConstants.UPLOAD_FOLDER.value, filename)


        with open(temp_path, 'wb') as f:
            f.write(image_data)

        user = UserRepository.get_user_by_username(username)

        if not user:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND,
                                            params={'resource': AppConstants.USER_RESOURCE.value})

        embedding_list = FaceRecognitionService._generate_embedding(temp_path)

        existing_embedding = FaceEmbeddingsRepository.get_face_embeddings(user.id)

        if existing_embedding:
            FaceEmbeddingsRepository.update_face_embeddings(existing_embedding, embedding_list)
        else:
            FaceEmbeddingsRepository.save_face_embeddings(user.id, embedding_list)

            UserRepository.mark_done_register_face(user)

        db.session.commit()

        if os.path.exists(temp_path):
            os.remove(temp_path)

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
