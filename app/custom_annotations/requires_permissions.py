from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def requires_role(required_role):
    """
    Dekorator sprawdzający czy JWT zawiera daną rolę.
    """

    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            print("JWT claims:", claims)  # Debug
            roles = claims.get("roles", [])
            if required_role not in roles:
                return (
                    jsonify({"msg": f"Forbidden – role '{required_role}' required"}),
                    403,
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
