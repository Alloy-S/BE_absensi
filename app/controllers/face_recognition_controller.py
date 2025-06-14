import os
import base64
import uuid
from flask import request, Blueprint
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename
from app.services.face_recognition_service import FaceRecognitionService
from app.utils.app_constans import AppConstants

os.makedirs(AppConstants.UPLOAD_FOLDER.value, exist_ok=True)

face_recognition_bp = Blueprint('face_recognition_bp', __name__, url_prefix='/api/face-recognition')
face_recognition_api = Api(face_recognition_bp)

class FaceRegistrationController(Resource):
    def post(self, user_id):

        json_data = request.get_json()
        if not json_data or 'image' not in json_data:
            return {'message': "Payload JSON tidak valid atau key 'image' tidak ditemukan."}, 400

        base64_string = json_data['image']

        try:
            if "," in base64_string:
                _, base64_data = base64_string.split(",", 1)
            else:
                base64_data = base64_string

            image_data = base64.b64decode(base64_data)
        except (ValueError, TypeError):
            return {'message': 'Format string Base64 tidak valid.'}, 400

        filename = f"{uuid.uuid4()}.jpg"
        temp_path = os.path.join(AppConstants.UPLOAD_FOLDER.value, filename)

        try:
            with open(temp_path, 'wb') as f:
                f.write(image_data)

            FaceRecognitionService.register_face(user_id=user_id, image_path=temp_path)

            return {'message': 'Wajah berhasil didaftarkan'}, 201

        except ValueError as e:
            return {'message': str(e)}, 400
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


class FaceRegistrationVerifyController(Resource):
    def post(self, user_id):
        json_data = request.get_json()
        if not json_data or 'image' not in json_data:
            return {'message': "Payload JSON tidak valid atau key 'image' tidak ditemukan."}, 400

        base64_string = json_data['image']

        try:
            if "," in base64_string:
                _, base64_data = base64_string.split(",", 1)
            else:
                base64_data = base64_string

            image_data = base64.b64decode(base64_data)
        except (ValueError, TypeError):
            return {'message': 'Format string Base64 tidak valid.'}, 400

        filename = f"{uuid.uuid4()}.jpg"
        temp_path = os.path.join(AppConstants.UPLOAD_FOLDER.value, filename)

        try:
            with open(temp_path, 'wb') as f:
                f.write(image_data)

            is_verified = FaceRecognitionService.verify_face(user_id=user_id, image_path=temp_path)

            if is_verified:
                return {'message': 'Wajah memiliki kecocokan', 'verified': True}, 200
            else:
                return {'message': 'Wajah tidak memiliki kecocokan', 'verified': False}, 200

        except ValueError as e:
            return {'message': str(e)}, 400
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

face_recognition_api.add_resource(FaceRegistrationController, '/register/<string:user_id>')
face_recognition_api.add_resource(FaceRegistrationVerifyController, '/verify/<string:user_id>')