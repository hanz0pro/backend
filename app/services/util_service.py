from app.models import User
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def get_user_count():
    """
    Zwraca liczbę użytkowników w bazie danych.

    Returns:
        int: Całkowita liczba rekordów w tabeli `User`.

    Example:
        >>> get_user_count()
        42
    """
    return User.query.count()


def get_debug_token_info():
    """
    Weryfikuje i zwraca informacje o bieżącym tokenie JWT.

    Returns:
        tuple: (response, status_code)

        - ({"msg": "Token OK", "user_id": <id>}, 200)
            gdy token jest poprawny

        - ({"msg": "Token ERROR", "details": "<szczegóły>"}, 422)
            gdy token jest niepoprawny lub brak nagłówka `Authorization`

    Example (poprawny token):
        {
          "msg": "Token OK",
          "user_id": 1
        }

    Example (błędny token):
        {
          "msg": "Token ERROR",
          "details": "Missing Authorization Header"
        }
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return {"msg": "Token OK", "user_id": user_id}, 200
    except Exception as e:
        return {"msg": "Token ERROR", "details": str(e)}, 422
