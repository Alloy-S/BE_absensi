import os
import uuid
from flask import request, Blueprint
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from app.services.face_recognition_service import FaceRecognitionService

UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

face_recognition_bp = Blueprint('face_recognition_bp', __name__, url_prefix='/api/face-recognition')
face_recognition_api = Api(face_recognition_bp)

class FaceRegistrationController(Resource):
    def post(self, user_id):

        if 'face_image' not in request.files:
            return {'message': "Bagian 'face_image' tidak ditemukan dalam request"}, 400

        file = request.files['face_image']

        if file.filename == '':
            return {'message': 'Tidak ada file yang dipilih'}, 400

        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        temp_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            file.save(temp_path)

            FaceRecognitionService.register_face(user_id=user_id, image_path=temp_path)

            return {'message': 'Wajah berhasil didaftarkan'}, 201

        except ValueError as e:
            return {'message': str(e)}, 400

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class FaceRegistrationVerifyController(Resource):
    def post(self, user_id):
        if 'face_image' not in request.files:
            return {'message': "Bagian 'face_image' tidak ditemukan dalam request"}, 400

        file = request.files['face_image']

        if file.filename == '':
            return {'message': 'Tidak ada file yang dipilih'}, 400

        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        temp_path = os.path.join(UPLOAD_FOLDER, filename)

        try:
            file.save(temp_path)

            if FaceRecognitionService.verify_face(user_id=user_id, image_path=temp_path):

                return {'message': 'Wajah Memiliki Kecocokan'}, 200
            else:
                return {'message': 'Wajah Tidak Memiliki Kecocokan'}, 200

        except ValueError as e:
            return {'message': str(e)}, 400

        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

face_recognition_api.add_resource(FaceRegistrationController, '/register/<string:user_id>')
face_recognition_api.add_resource(FaceRegistrationVerifyController, '/verify/<string:user_id>')