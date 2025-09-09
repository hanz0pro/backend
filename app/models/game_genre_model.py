from app import db

#: Tabela asocjacyjna łącząca gry z gatunkami (relacja wiele-do-wielu).
#:
#: Każdy rekord odpowiada przypisaniu konkretnej gry do konkretnego gatunku.
#:
#: - `game_id` → ID gry (`Game.id`)
#: - `genre_id` → ID gatunku (`Genre.id`)
game_genre = db.Table(
    "game_genre",
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True),
)


class Genre(db.Model):
    """
    Model reprezentujący gatunek gry.

    Atrybuty:
        id (int): Unikalny identyfikator gatunku (klucz główny).
        name (str): Nazwa gatunku. Musi być unikalna i niepusta
            (np. `"RPG"`, `"Action"`, `"Strategy"`).

    Relacje:
        games (list[Game]): Lista gier przypisanych do tego gatunku
            (poprzez tabelę pośredniczącą `game_genre`).

    Example:
        ```python
        # utworzenie nowego gatunku
        genre = Genre(name="RPG")
        db.session.add(genre)
        db.session.commit()

        # pobranie wszystkich gier z tego gatunku
        rpg_games = genre.games.all()
        ```
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        """Reprezentacja tekstowa gatunku (przydatna do debugowania)."""
        return f"<Genre(name='{self.name}')>"
