from app import db

#: Tabela asocjacyjna łącząca użytkowników z rolami (relacja wiele-do-wielu).
#:
#: Każdy rekord odpowiada przypisaniu konkretnej roli do konkretnego użytkownika.
#:
#: - `user_id` → ID użytkownika (`User.id`)
#: - `role_id` → ID roli (`Role.id`)
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)


class Role(db.Model):
    """
    Model reprezentujący rolę przypisaną do użytkowników.

    Atrybuty:
        id (int): Unikalny identyfikator roli (klucz główny).
        name (str): Nazwa roli. Musi być unikalna i niepusta
            (np. `"admin"`, `"moderator"`, `"user"`).

    Relacje:
        users (list[User]): Lista użytkowników posiadających tę rolę.
            Relacja wiele-do-wielu poprzez tabelę pośredniczącą `user_roles`.

    Example:
        ```python
        # Utworzenie nowej roli
        role = Role(name="admin")
        db.session.add(role)
        db.session.commit()

        # Przypisanie roli do użytkownika
        user = User.query.get(1)
        user.roles.append(role)
        db.session.commit()

        # Pobranie wszystkich użytkowników z daną rolą
        admins = role.users
        ```
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    users = db.relationship("User", secondary=user_roles, back_populates="roles")

    def __repr__(self):
        return f"<Role(name='{self.name}')>"
