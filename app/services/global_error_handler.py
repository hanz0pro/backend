from flask import Blueprint, jsonify
from werkzeug.exceptions import (
    BadRequest,
    NotFound,
    MethodNotAllowed,
    InternalServerError,
    Unauthorized,
)

error_bp = Blueprint("error_bp", __name__)


# Obsługa znanych błędów HTTP
@error_bp.app_errorhandler(BadRequest)
def handle_400(error):
    """
    Obsługuje błąd 400 Bad Request.

    Response (400 Bad Request):
        {
            "error": "Bad Request",
            "message": "Opis błędu"
        }
    """
    return jsonify(error="Bad Request", message=str(error)), 400


@error_bp.app_errorhandler(NotFound)
def handle_404(error):
    """
    Obsługuje błąd 404 Not Found.

    Response (404 Not Found):
        {
            "error": "Not Found",
            "message": "Żądany zasób nie istnieje."
        }
    """
    return jsonify(error="Not Found", message=str(error)), 404


@error_bp.app_errorhandler(Unauthorized)
def handle_401(error):
    """
    Obsługuje błąd 401 Unauthorized.

    Response (401 Unauthorized):
        {
            "error": "Unauthorized",
            "message": "Brak autoryzacji lub niepoprawny token."
        }
    """
    return jsonify(error="Unauthorized", message=str(error)), 401


@error_bp.app_errorhandler(MethodNotAllowed)
def handle_405(error):
    """
    Obsługuje błąd 405 Method Not Allowed.

    Response (405 Method Not Allowed):
        {
            "error": "Method Not Allowed",
            "message": "Metoda HTTP nie jest dozwolona dla tego zasobu."
        }
    """
    return jsonify(error="Method Not Allowed", message=str(error)), 405


@error_bp.app_errorhandler(InternalServerError)
def handle_500(error):
    """
    Obsługuje błąd 500 Internal Server Error.

    Response (500 Internal Server Error):
        {
            "error": "Internal Server Error",
            "message": "Coś poszło nie tak."
        }
    """
    return jsonify(error="Internal Server Error", message="Coś poszło nie tak."), 500


# Obsługa wszystkich innych wyjątków
@error_bp.app_errorhandler(Exception)
def handle_exception(error):
    """
    Obsługuje wszystkie inne, nieprzewidziane wyjątki.

    Response (500 Internal Server Error):
        {
            "error": "Unexpected Error",
            "message": "Szczegóły wyjątku"
        }
    """
    return jsonify(error="Unexpected Error", message=str(error)), 500
