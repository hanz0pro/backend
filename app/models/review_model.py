from app import db


class Review(db.Model):
    """
    Model reprezentujący recenzję gry dodaną przez użytkownika.

    Atrybuty:
        id (int): Unikalny identyfikator recenzji (klucz główny).
        rating (int): Ocena gry wyrażona liczbą całkowitą (np. 1–5).
        comment (str): Opcjonalny komentarz użytkownika do gry.

        user_id (int): Klucz obcy do tabeli `user`. Określa, który użytkownik
            dodał recenzję.
        game_id (int): Klucz obcy do tabeli `game`. Określa, której gry dotyczy recenzja.

    Relacje:
        user (User): Użytkownik, który wystawił recenzję.
        game (Game): Gra, której dotyczy recenzja.

    Example:
        ```python
        # Utworzenie nowej recenzji
        review = Review(rating=5, comment="Świetna gra!", user_id=1, game_id=10)
        db.session.add(review)
        db.session.commit()

        # Pobranie recenzji użytkownika
        user_reviews = Review.query.filter_by(user_id=1).all()

        # Pobranie recenzji dla gry
        game_reviews = Review.query.filter_by(game_id=10).all()
        ```

    Note:
        - Każdy użytkownik może dodać **tylko jedną recenzję** do danej gry
          (logika powinna być kontrolowana w endpointzie).
        - Relacja `Review` → `User` i `Review` → `Game` jest wiele-do-jednego.
    """

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
