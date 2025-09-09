from app.models import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def get_user_count():
    return User.query.count()


def get_debug_token_info():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return {"msg": "Token OK", "user_id": user_id}, 200
    except Exception as e:
        return {"msg": "Token ERROR", "details": str(e)}, 422
