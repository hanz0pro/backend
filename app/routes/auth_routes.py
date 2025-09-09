from flask import request, jsonify
from . import api
from app.services.user_service import register_user, login_user


@api.route("/auth/register", methods=["POST"])
def register():
    """
    Endpoint rejestracji nowego użytkownika.

    Request JSON:
        {
            "username": "string",   # wymagane, unikalna nazwa użytkownika
            "password": "string"    # wymagane, hasło użytkownika (zostanie zahashowane)
        }

    Response (201 Created):
        {
            "msg": "User registered successfully",
            "user": {
                "id": 1,
                "username": "janek"
            }
        }

    Response (400 Bad Request):
        {
            "error": "Username and password are required"
        }

    Response (409 Conflict):
        {
            "error": "User already exists"
        }

    Returns:
        tuple: JSON response oraz kod HTTP.
    """
    data = request.json
    response, status = register_user(data)
    return jsonify(response), status


@api.route("/auth/login", methods=["POST"])
def login():
    """
    Endpoint logowania użytkownika.

    Request JSON:
        {
            "username": "string",   # wymagane, nazwa użytkownika
            "password": "string"    # wymagane, hasło użytkownika
        }

    Response (200 OK):
        {
            "access_token": "jwt-token-string",
            "roles": ["user", "admin"]
        }

    Response (401 Unauthorized):
        {
            "error": "Invalid username or password"
        }

    Returns:
        tuple: JSON response zawierający token JWT (przy poprawnym logowaniu)
        lub błąd z odpowiednim kodem HTTP.
    """
    data = request.json
    response, status = login_user(data)
    return jsonify(response), status
