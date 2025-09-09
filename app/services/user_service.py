from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import User, Role


def register_user(data):
    """
    Rejestruje nowego użytkownika w systemie.

    Args:
        data (dict): Dane wejściowe w formacie:
            {
              "username": "string",  # wymagane, unikalna nazwa użytkownika
              "password": "string"   # wymagane, hasło w postaci jawnej (zostanie zahashowane)
            }

    Returns:
        tuple: (response, status_code)
            - ({"msg": "User created"}, 201) – jeśli rejestracja się powiodła
            - ({"msg": "User already exists"}, 409) – jeśli użytkownik o takiej nazwie już istnieje

    Note:
        - Hasło użytkownika jest zapisywane w bazie w postaci **hashu** (bcrypt).
        - Nowy użytkownik automatycznie otrzymuje domyślną rolę `"user"` (o ile istnieje w tabeli `Role`).
    """

    if User.query.filter_by(username=data["username"]).first():
        return {"msg": "User already exists"}, 409

    hashed_pw = generate_password_hash(data["password"])
    user = User(username=data["username"], password=hashed_pw)

    # 🔐 przypisz domyślną rolę "user"
    default_role = Role.query.filter_by(name="user").first()
    if default_role:
        user.roles.append(default_role)

    db.session.add(user)
    db.session.commit()

    return {"msg": "User created"}, 201


def login_user(data):
    """
    Loguje istniejącego użytkownika i zwraca token JWT.

    Args:
        data (dict): Dane wejściowe w formacie:
            {
              "username": "string",  # wymagane, nazwa użytkownika
              "password": "string"   # wymagane, hasło w postaci jawnej
            }

    Returns:
        tuple: (response, status_code)
            - ({"access_token": "<jwt>"}, 200) – jeśli dane poprawne
            - ({"msg": "Invalid credentials"}, 401) – jeśli login/hasło nieprawidłowe

    Note:
        - Do tokenu JWT dodawane są role użytkownika w polu `roles`.
        - W `identity` tokenu zapisywany jest `user.id` (jako string).
        - Token JWT należy przesyłać w nagłówku:
            `Authorization: Bearer <token>`.
    """
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        # Pobierz nazwy ról
        role_names = [role.name for role in user.roles]

        # Tworzymy token z dodatkowymi claims (rolami)
        token = create_access_token(
            identity=str(user.id), additional_claims={"roles": role_names}
        )

        return {"access_token": token}, 200

    return {"msg": "Invalid credentials"}, 401
