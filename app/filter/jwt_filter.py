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

            user_roles = [r.role.name for r in user.user_role]

            if user is None or not set(user_roles).intersection(set(roles)):
                return {'message': 'Unauthorized'}, 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper


def permission_required(required_permission):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_permissions = claims.get('permissions', [])

            if required_permission not in user_permissions:
                return {'message': 'Unauthorized'}, 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper