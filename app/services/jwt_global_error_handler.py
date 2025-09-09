from flask import jsonify
from flask_jwt_extended import JWTManager


def register_jwt_error_handlers(app):
    """
    Rejestruje globalne handlery błędów JWT dla aplikacji Flask.

    Obsługuje typowe sytuacje związane z tokenami JWT:
      - brak nagłówka autoryzacji,
      - niepoprawny token,
      - wygasły token,
      - cofnięty token,
      - wymagany świeży token.

    Args:
        app (Flask): instancja aplikacji Flask.

    Returns:
        JWTManager: obiekt JWTManager z przypiętymi handlerami błędów.
    """
    jwt = JWTManager(app)

    @jwt.unauthorized_loader
    def handle_missing_token(reason):
        """
        Brak nagłówka `Authorization`.

        Response (401 Unauthorized):
            {
              "error": "Unauthorized",
              "message": "Brakuje nagłówka autoryzacji (Authorization header)."
            }
        """
        return (
            jsonify(
                error="Unauthorized",
                message="Brakuje nagłówka autoryzacji (Authorization header).",
            ),
            401,
        )

    @jwt.invalid_token_loader
    def handle_invalid_token(reason):
        """
        Niepoprawny token JWT.

        Response (422 Unprocessable Entity):
            {
              "error": "Invalid Token",
              "message": "<powód>"
            }
        """
        return jsonify(error="Invalid Token", message=reason), 422

    @jwt.expired_token_loader
    def handle_expired_token(jwt_header, jwt_payload):
        """
        Wygasły token JWT.

        Response (401 Unauthorized):
            {
              "error": "Token Expired",
              "message": "Token JWT wygasł."
            }
        """
        return jsonify(error="Token Expired", message="Token JWT wygasł."), 401

    @jwt.revoked_token_loader
    def handle_revoked_token(jwt_header, jwt_payload):
        """
        Cofnięty (unieważniony) token JWT.

        Response (401 Unauthorized):
            {
              "error": "Revoked Token",
              "message": "Token został cofnięty."
            }
        """
        return jsonify(error="Revoked Token", message="Token został cofnięty."), 401

    @jwt.needs_fresh_token_loader
    def handle_fresh_token_required(jwt_header, jwt_payload):
        """
        Wymagany świeży token JWT.

        Response (401 Unauthorized):
            {
              "error": "Fresh Token Required",
              "message": "Wymagany świeży token JWT."
            }
        """
        return (
            jsonify(error="Fresh Token Required", message="Wymagany świeży token JWT."),
            401,
        )

    return jwt
