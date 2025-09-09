from functools import wraps

from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt


def requires_role(required_role):
    """
    Dekorator sprawdzający, czy użytkownik (na podstawie JWT) posiada wymaganą rolę.

    Args:
        required_role (str): Nazwa roli wymagana do wykonania danego endpointu
            (np. `"admin"`, `"moderator"`, `"user"`).

    Returns:
        function: Ozdobiona funkcja widoku Flask, która:
            - sprawdza obecność i poprawność tokenu JWT (`@jwt_required()`),
            - weryfikuje, czy w polu `roles` JWT znajduje się `required_role`,
            - jeśli rola jest obecna → wywołuje oryginalny endpoint,
            - jeśli rola jest nieobecna → zwraca odpowiedź JSON z kodem HTTP 403.

    Example:
        ```python
        @app.route("/admin/dashboard")
        @requires_role("admin")
        def admin_dashboard():
            return jsonify({"msg": "Witaj w panelu admina!"})
        ```

        W powyższym przykładzie:
        - użytkownik z JWT, które zawiera `{"roles": ["admin"]}` → uzyska dostęp,
        - użytkownik bez roli `"admin"` → dostanie `403 Forbidden`.

    Note:
        Wymaga, aby podczas generowania tokenu JWT dołączyć pole `"roles"`,
        np. w `create_access_token(identity=user.id, additional_claims={"roles": ["admin"]})`.
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
