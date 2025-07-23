import base64
import os
import uuid
from app.repositories.user_repository import UserRepository
from app.repositories.reimburse_repository import ReimburseRepository
from app.repositories.photo_repository import PhotoRepository
from app.database import db
from app.utils.app_constans import AppConstants
from app.utils.error_code import ErrorCode
from app.execption.custom_execption import GeneralException, GeneralExceptionWithParam

class PhotoService:

    @staticmethod
    def save_photo(base64_string: str):

        if not base64_string or not isinstance(base64_string, str):
            raise ValueError("Input harus berupa string Base64 yang tidak kosong.")

        try:
            if "," in base64_string:
                header, base64_data = base64_string.split(",", 1)
                mimetype = header.split(';')[0].split(':')[1]
            else:
                base64_data = base64_string
                mimetype = 'application/octet-stream'

            image_data = base64.b64decode(base64_data)
        except (ValueError, TypeError):
            return {'message': 'Format string Base64 tidak valid.'}, 400

        file_type = mimetype.split('/')[1]
        unique_filename = f"{uuid.uuid4()}.{file_type}"
        file_path = os.path.join(AppConstants.UPLOAD_FOLDER_PHOTO.value, unique_filename)

        try:
            with open(file_path, 'wb') as f:
                f.write(image_data)
        except IOError:
            return {'message': 'Gagal menyimpan file di server.'}, 500

        photo = PhotoRepository.create({
            'type': AppConstants.REIMBURSE_RESOURCE.value,
            'path': file_path,
            'filename': unique_filename,
            'mimetype': mimetype
        })

        db.session.commit()

        return photo

    @staticmethod
    def delete_photo(photo_id: str):

        photo_to_delete = PhotoRepository.get_photo_by_id(photo_id)
        if not photo_to_delete:
            raise ValueError("Foto tidak ditemukan.")

        file_path = photo_to_delete.path

        PhotoRepository.delete_photo(photo_to_delete)

        try:
            if os.path.exists(file_path):
                os.remove(file_path)

            db.session.commit()
        except OSError as e:
            print(f"Error saat menghapus file {file_path}: {e}")

    @staticmethod
    def get_photo_as_base64(photo_id):
        if not photo_id:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.PHOTO_RESOURCE.value})

        photo = PhotoRepository.get_photo_by_id(photo_id)
        if not photo or not os.path.exists(photo.path):
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.PHOTO_RESOURCE.value})

        try:
            with open(photo.path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

            return {
                "id": photo_id,
                "filename": photo.filename,
                "type": photo.type,
                "mimetype": photo.mimetype,
                "image": f"data:{photo.mimetype};base64,{encoded_string}",
            }
        except Exception:
            raise GeneralExceptionWithParam(ErrorCode.RESOURCE_NOT_FOUND, params={'resource': AppConstants.PHOTO_RESOURCE.value})
