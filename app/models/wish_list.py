from app import db


class WishList(db.Model):
    """
    Model reprezentujący wpis na liście życzeń użytkownika.

    Atrybuty:
        id (int): Unikalny identyfikator wpisu (klucz główny).
        user_id (int): Klucz obcy do tabeli `user`. Określa właściciela wpisu na liście życzeń.
        game_id (int): Klucz obcy do tabeli `game`. Określa grę dodaną do wishlisty.

    Relacje:
        user (User): Użytkownik, który dodał grę do swojej listy życzeń.
        game (Game): Gra, która została dodana do listy życzeń.

    Example:
        ```python
        # Dodanie gry do wishlisty użytkownika
        wishlist_entry = WishList(user_id=1, game_id=10)
        db.session.add(wishlist_entry)
        db.session.commit()

        # Pobranie wishlisty użytkownika
        user_wishlist = WishList.query.filter_by(user_id=1).all()

        # Pobranie wszystkich użytkowników, którzy mają grę w wishlist
        game_wishlist = WishList.query.filter_by(game_id=10).all()
        ```

    Note:
        - Każdy użytkownik może mieć wiele gier na wishliście.
        - Jeśli użytkownik lub gra zostaną usunięci, powiązane wpisy
          z wishlisty są również usuwane dzięki kaskadzie w relacjach.
    """

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
