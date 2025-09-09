from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User
from app.models.game_model import Game
from app.models.review_model import Review
from app.routes import api


def validate_rating(value):
    """
    Waliduje ocenę gry.

    Args:
        value (int|str): Wartość do sprawdzenia.

    Returns:
        int|None: Ocena (1..5) jeśli poprawna, inaczej None.
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return None
    return value if 1 <= value <= 5 else None


@api.route("/games/<int:game_id>/review", methods=["POST"])
@jwt_required()
def upsert_review(game_id):
    """
    Dodaje lub aktualizuje recenzję gry dla zalogowanego użytkownika.

    Request JSON:
        {
          "rating": 5,            # wymagane, liczba całkowita 1..5
          "comment": "Świetna!"   # opcjonalne, string
        }

    Response (201 Created) – dodano nową recenzję:
        {
          "message": "Recenzja dodana.",
          "review": {
            "id": 1,
            "user_id": 3,
            "game_id": 10,
            "rating": 5,
            "comment": "Świetna!"
          }
        }

    Response (200 OK) – zaktualizowano istniejącą recenzję:
        {
          "message": "Recenzja zaktualizowana.",
          "review": { ... }
        }

    Response (400 Bad Request):
        {"message": "Pole 'rating' musi być liczbą całkowitą 1..5."}

    Response (404 Not Found):
        {"message": "Gra nie istnieje."}

    Response (500 Internal Server Error):
        {"message": "Nie udało się zapisać recenzji."}
    """
    data = request.get_json(silent=True) or {}
    rating = validate_rating(data.get("rating"))
    comment = (data.get("comment") or "").strip()

    if rating is None:
        return (
            jsonify({"message": "Pole 'rating' musi być liczbą całkowitą 1..5."}),
            400,
        )

    # Sprawdź czy gra istnieje
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"message": "Gra nie istnieje."}), 404

    user_id = get_jwt_identity()  # zakładam, że tu trzymasz user_id

    try:
        # Spróbuj znaleźć istniejącą recenzję
        review = Review.query.filter_by(user_id=user_id, game_id=game_id).first()

        if review:
            # UPDATE
            review.rating = rating
            review.comment = comment
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "Recenzja zaktualizowana.",
                        "review": {
                            "id": review.id,
                            "user_id": review.user_id,
                            "game_id": review.game_id,
                            "rating": review.rating,
                            "comment": review.comment,
                        },
                    }
                ),
                200,
            )
        else:
            # INSERT
            review = Review(
                user_id=user_id, game_id=game_id, rating=rating, comment=comment
            )
            db.session.add(review)
            db.session.commit()
            return (
                jsonify(
                    {
                        "message": "Recenzja dodana.",
                        "review": {
                            "id": review.id,
                            "user_id": review.user_id,
                            "game_id": review.game_id,
                            "rating": review.rating,
                            "comment": review.comment,
                        },
                    }
                ),
                201,
            )

    except Exception as e:
        db.session.rollback()
        # Jeżeli constraint zadziałał i złapiesz IntegrityError, możesz zwrócić 409.
        # Żeby nie wyciekać szczegółów DB, zwróć ogólny komunikat:
        return jsonify({"message": "Nie udało się zapisać recenzji."}), 500


@api.route("/users/me/reviews", methods=["GET"])
@jwt_required()
def get_my_reviews():
    """
    Pobiera wszystkie recenzje zalogowanego użytkownika.

    Request:
        Wymaga JWT.

    Response (200 OK):
        [
          {
            "id": 1,
            "game_id": 10,
            "game_title": "Wiedźmin 3",
            "rating": 5,
            "comment": "Świetna!"
          },
          ...
        ]
    """
    user_id = get_jwt_identity()

    reviews = (
        db.session.query(Review)
        .join(Game, Review.game_id == Game.id)
        .filter(Review.user_id == user_id)
        .all()
    )

    result = [
        {
            "id": r.id,
            "game_id": r.game_id,
            "game_title": r.game.title if r.game else None,
            "rating": r.rating,
            "comment": r.comment,
        }
        for r in reviews
    ]

    return jsonify(result), 200


@api.route("games/<int:game_id>/reviews", methods=["GET"])
def get_game_reviews(game_id):
    """
    Pobiera wszystkie recenzje dla wybranej gry.

    Args:
        game_id (int): ID gry.

    Response (200 OK):
        [
          {
            "id": 1,
            "user_id": 3,
            "username": "janek",
            "rating": 5,
            "comment": "Świetna!"
          },
          ...
        ]
    """
    rows = (
        db.session.query(Review, User.username)
        .join(User, Review.user_id == User.id)
        .filter(Review.game_id == game_id)
        .order_by(Review.id.desc())
        .all()
    )
    data = [
        {
            "id": r.id,
            "user_id": r.user_id,
            "username": username,
            "rating": r.rating,
            "comment": r.comment,
        }
        for r, username in rows
    ]
    return jsonify(data), 200
