from flask import Blueprint
from flask_restful import Api, Resource, marshal_with

notification_bp = Blueprint('notification_bp', __name__, url_prefix='/api/notification')
notification_bp = Api(notification_bp)

class NotificationController(Resource):

    @staticmethod
    def post():
        print("POST")