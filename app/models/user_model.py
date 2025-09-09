from app import db
from app.models.role_model import user_roles


class User(db.Model):
    """
    Model reprezentujący użytkownika systemu.

    Atrybuty:
        id (int): Unikalny identyfikator użytkownika (klucz główny).
        username (str): Nazwa użytkownika. Musi być unikalna i niepusta.
        password (str): Hasło użytkownika, przechowywane w postaci zahashowanej
            (np. bcrypt, Argon2 itp.).

    Relacje:
        reviews (list[Review]): Lista recenzji wystawionych przez użytkownika.
            Relacja jeden-do-wielu z modelem `Review`. Usunięcie użytkownika usuwa jego recenzje.
        wishlist (list[WishList]): Lista gier zapisanych przez użytkownika do listy życzeń.
            Relacja jeden-do-wielu z modelem `WishList`. Usunięcie użytkownika usuwa jego wishlistę.
        roles (list[Role]): Lista ról przypisanych do użytkownika.
            Relacja wiele-do-wielu poprzez tabelę pośredniczącą `user_roles`.

    Example:
        ```python
        # Utworzenie nowego użytkownika
        user = User(username="janek", password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # Dodanie roli do użytkownika
        role = Role.query.filter_by(name="admin").first()
        user.roles.append(role)
        db.session.commit()

        # Pobranie wszystkich recenzji użytkownika
        my_reviews = user.reviews
        ```

    Note:
        - Hasło **zawsze** należy przechowywać w postaci zahashowanej.
        - Rola użytkownika jest przechowywana w relacji wiele-do-wielu.
        - Jeśli usuniemy użytkownika, kaskadowo zostaną usunięte jego recenzje
          oraz wpisy z wishlisty.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    reviews = db.relationship(
        "Review", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    wishlist = db.relationship(
        "WishList", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    roles = db.relationship("Role", secondary=user_roles, back_populates="users")
