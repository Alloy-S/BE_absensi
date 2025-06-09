from flask_restful import Resource, Api, marshal_with
from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from app.services.auth_service import AuthService
from app.models.auth.login_req import LoginReq
from app.models.auth.login_res import login_res

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')
auth_api = Api(auth_bp)


class LoginController(Resource):

    @marshal_with(login_res)
    def post(self):
        try:
            schema = LoginReq()
            req = schema.load(request.get_json())
            user = AuthService.authenticate_user(req['username'], req['password'])
            if not user:
                return {'message': 'Invalid username or password'}, 401

            access_token = create_access_token(
                identity=user.username,
                additional_claims={
                    'name': user.fullname,
                    'role': user.user_role.name
                },
                expires_delta=False
            )

            response = {
                'token': access_token,
                'username': user.username,
                'fullname': user.fullname,
                'role': user.user_role.name
            }
            return response, 200

        except Exception as _:
            return {'message': 'Internal server error'}, 500


auth_api.add_resource(LoginController, '/login')
