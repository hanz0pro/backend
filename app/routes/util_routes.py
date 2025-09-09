from flask import jsonify
from . import api
from app.services.util_service import get_user_count, get_debug_token_info
from ..custom_annotations import requires_role


@api.route("/", methods=["GET"])
def index():
    """
    Strona główna API.

    Request:
        Brak parametrów.

    Response (200 OK):
        {
            "message": "Welcome to the API!"
        }
    """
    return jsonify({"message": "Welcome to the API!"}), 200


@api.route("/health", methods=["GET"])
def health():
    """
    Prosty health-check aplikacji.

    Request:
        Brak parametrów.

    Response (200 OK):
        {
            "status": "ok"
        }
    """
    return jsonify({"status": "ok"}), 200


@api.route("/db-check", methods=["GET"])
@requires_role("admin")
def db_check():
    """
    Sprawdzenie stanu bazy danych (tylko dla admina).

    Wymaga roli `"admin"` w JWT.

    Response (200 OK):
        {
            "db": "ok",
            "users": 42
        }

    Response (500 Internal Server Error):
        {
            "db": "error",
            "details": "komunikat błędu"
        }
    """
    try:
        count = get_user_count()
        return jsonify({"db": "ok", "users": count}), 200
    except Exception as e:
        return jsonify({"db": "error", "details": str(e)}), 500


@api.route("/admin/only", methods=["GET"])
@requires_role("admin")
def admin_only_endpoint():
    """
    Przykładowy endpoint dostępny tylko dla adminów.

    Wymaga roli `"admin"` w JWT.

    Response (200 OK):
        {
            "msg": "Witaj adminie!"
        }
    """
    return jsonify({"msg": "Witaj adminie!"})


@api.route("/debug-token", methods=["GET"])
def debug_token():
    """
    Debugowanie tokenu JWT – zwraca informacje o aktualnym tokenie.

    Request:
        Wymaga przekazania JWT w nagłówku Authorization.

    Response (200 OK):
        {
            "identity": 1,
            "roles": ["admin"],
            "exp": 1736424000
        }

    Response (401 Unauthorized):
        {"msg": "Missing Authorization Header"}
    """
    response, code = get_debug_token_info()
    return jsonify(response), code


@api.route("/.well-known/appspecific/com.chrome.devtools.json")
def ignore_devtools_probe():
    """
    Ignoruje automatyczne żądania DevTools (np. Chrome/Brave).
    Zawsze zwraca pustą odpowiedź.

    Response (204 No Content):
        (brak treści)
    """
    return "", 204
