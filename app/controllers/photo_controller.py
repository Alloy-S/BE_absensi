from flask_jwt_extended import get_jwt_identity
from app.filter.jwt_filter import role_required
from app.utils.app_constans import AppConstants
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.photo_service import PhotoService
from app.models.photo.photo_res import photo_field

photo_bp = Blueprint('photo_bp', __name__, url_prefix='/api/photo')
photo_api = Api(photo_bp)

class PhotoByIdController(Resource):

    @role_required(AppConstants.USER_GROUP.value)
    def get(self, photo_id):

        response = PhotoService.get_photo_as_base64(photo_id)

        return marshal(response, photo_field), 200


photo_api.add_resource(PhotoByIdController, '/<string:photo_id>')