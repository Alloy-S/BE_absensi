from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.services.user_service import UserService

def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()

            username = claims['sub']

            user = UserService.get_user_by_username(username)
            print(username)
            print(roles)

            if user is None or user.user_role.name not in roles:
                return {'message': 'Unauthorized'}, 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper