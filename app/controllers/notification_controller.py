from flask_restful import Resource


class NotificationController(Resource):
    def post(self):

        return {}, 200