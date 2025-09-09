from app import db
from app.models.game_genre_model import game_genre
from app.models.game_tag_model import game_tag


class Game(db.Model):
    """
    Model reprezentujący grę w systemie.

    Atrybuty:
        id (int): Unikalny identyfikator gry (klucz główny).
        title (str): Tytuł gry. Wymagany i unikalny (np. "Wiedźmin 3").
        description (str): Opcjonalny opis gry.
        price (float): Cena gry w pełnej wartości (bez zniżki).
        discount (float): Zniżka (%) przypisana do gry. Może być `NULL` lub 0,
            np. `20.0` oznacza 20% rabatu.
        image_path (str): Ścieżka względna do obrazka gry (np. `"static/images/games/example.png"`).

    Relacje:
        genres (list[Genre]): Lista gatunków przypisanych do gry.
            Relacja wiele-do-wielu poprzez tabelę pośredniczącą `game_genre`.
        tags (list[Tag]): Lista tagów przypisanych do gry.
            Relacja wiele-do-wielu poprzez tabelę pośredniczącą `game_tag`.
        reviews (list[Review]): Lista recenzji przypisanych do gry.
            Relacja jeden-do-wielu z modelem `Review`. Usunięcie gry usuwa również recenzje.
        wishlists (list[WishList]): Lista powiązań z listami życzeń użytkowników.
            Relacja jeden-do-wielu z modelem `WishList`. Usunięcie gry usuwa również wpisy z wishlist.

    Example:
        ```python
        # Utworzenie nowej gry
        game = Game(
            title="Wiedźmin 3",
            description="Gra RPG osadzona w świecie fantasy",
            price=199.99,
            discount=20.0,
            image_path="static/images/games/witcher3.png"
        )
        db.session.add(game)
        db.session.commit()

        # Dodanie gatunku do gry
        genre = Genre.query.filter_by(name="RPG").first()
        game.genres.append(genre)

        # Pobranie wszystkich recenzji gry
        reviews = game.reviews
        ```

    Note:
        - Cena końcowa do wyświetlenia na froncie może być obliczana jako:
          `price * (1 - discount / 100)`, jeśli `discount` jest różne od 0.
        - Pole `image_path` przechowuje ścieżkę względną (np. w katalogu `static`).
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    discount = db.Column(db.Float)
    image_path = db.Column(db.String(255))

    # wiele gatunków
    genres = db.relationship(
        "Genre", secondary=game_genre, backref=db.backref("games", lazy="dynamic")
    )
    # wiele tagów
    tags = db.relationship(
        "Tag", secondary=game_tag, backref=db.backref("games", lazy="dynamic")
    )

    reviews = db.relationship(
        "Review", backref="game", lazy=True, cascade="all, delete-orphan"
    )
    wishlists = db.relationship(
        "WishList", backref="game", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Game(title='{self.title}', price={self.price})>"
