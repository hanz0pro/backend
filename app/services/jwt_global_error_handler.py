from flask import jsonify
from flask_jwt_extended import JWTManager

def register_jwt_error_handlers(app):
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def handle_missing_token(reason):
        return jsonify(error="Unauthorized", message="Brakuje nagłówka autoryzacji (Authorization header)."), 401

    @jwt.invalid_token_loader
    def handle_invalid_token(reason):
        return jsonify(error="Invalid Token", message=reason), 422

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        return jsonify(error="Token Expired", message="Token JWT wygasł."), 401

    @jwt.revoked_token_loader
    def handle_revoked_token(jwt_header, jwt_payload):
        return jsonify(error="Revoked Token", message="Token został cofnięty."), 401

    @jwt.needs_fresh_token_loader
    def handle_fresh_token_required(jwt_header, jwt_payload):
        return jsonify(error="Fresh Token Required", message="Wymagany świeży token JWT."), 401

    return jwt
