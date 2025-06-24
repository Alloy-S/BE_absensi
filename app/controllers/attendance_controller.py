import base64
import uuid
import os
from flask_restful import Resource, Api, marshal
from flask import Blueprint, request
from app.services.attendance_service import AttendanceService
from app.models.attendance.attendance_req import AttendanceRequestSchema
from app.models.attendance.attendance_res import check_today_attendance
from app.utils.app_constans import AppConstants
from app.filter.jwt_filter import role_required
from flask_jwt_extended import get_jwt_identity

os.makedirs(AppConstants.UPLOAD_FOLDER.value, exist_ok=True)

attendance_bp = Blueprint('attendance_bp', __name__, url_prefix='/api/attendance')
attendance_api = Api(attendance_bp)


class AttendanceController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def post(self):
        current_username = get_jwt_identity()
        json_data = request.get_json()

        schema = AttendanceRequestSchema()

        validated_data = schema.load(json_data)

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


        with open(temp_path, 'wb') as f:
            f.write(image_data)

        response = AttendanceService.create_attendance(current_username, validated_data, temp_path)

        if os.path.exists(temp_path):
            os.remove(temp_path)

        return {'message': response}, 200

class CheckTodayAttendanceController(Resource):
    @role_required(AppConstants.USER_GROUP.value)
    def get(self):
        response = AttendanceService.check_today_attendance(get_jwt_identity())

        return marshal(response, check_today_attendance), 200


attendance_api.add_resource(AttendanceController, '')
attendance_api.add_resource(CheckTodayAttendanceController, '/today')