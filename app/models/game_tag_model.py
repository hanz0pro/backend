from app import db

#: Tabela asocjacyjna łącząca gry z tagami (relacja wiele-do-wielu).
#:
#: Każdy rekord odpowiada przypisaniu konkretnej gry do konkretnego taga.
#:
#: - `game_id` → ID gry (`Game.id`)
#: - `tag_id` → ID taga (`Tag.id`)
game_tag = db.Table(
    "game_tag",
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Tag(db.Model):
    """
    Model reprezentujący tag przypisany do gry.

    Atrybuty:
        id (int): Unikalny identyfikator taga (klucz główny).
        name (str): Nazwa taga. Musi być unikalna i niepusta
            (np. `"Singleplayer"`, `"Open World"`, `"Multiplayer"`).

    Relacje:
        games (list[Game]): Lista gier, które mają przypisany ten tag.
            Relacja wiele-do-wielu poprzez tabelę pośredniczącą `game_tag`.

    Example:
        ```python
        # Utworzenie nowego taga
        tag = Tag(name="Open World")
        db.session.add(tag)
        db.session.commit()

        # Pobranie wszystkich gier z tym tagiem
        open_world_games = tag.games.all()
        ```
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag(name='{self.name}')>"
