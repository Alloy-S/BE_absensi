from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from services.auth_service import AuthService
from repositories.user_repository import UserRepository

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True, help="Username cannot be blank")
auth_parser.add_argument('password', type=str, required=True, help="Password cannot be blank")

register_parser = auth_parser.copy()
register_parser.add_argument('name', type=str, required=True, help="Name cannot be blank")

class Login(Resource):
    def post(self):
        args = auth_parser.parse_args()
        user = AuthService.authenticate_user(args['username'], args['password'])
        if not user:
            return {'message': 'Invalid username or password'}, 401
        
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200

class Register(Resource):
    def post(self):
        args = register_parser.parse_args()
        # existing_user = UserRepository.get_user_by_email(args['username'])
        # if existing_user:
        #     return {'message': 'User already exists'}, 400

        user = UserRepository.create_user(args['name'], args['username'], args['password'])
        return {'message': 'User created successfully'}, 201