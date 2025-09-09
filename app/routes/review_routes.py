from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User
from app.models.game_model import Game
from app.models.review_model import Review
from app.routes import api


def validate_rating(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return None
    return value if 1 <= value <= 5 else None


@api.route("/games/<int:game_id>/review", methods=["POST"])
@jwt_required()
def upsert_review(game_id):
    """
    Body (JSON):
    {
      "rating": 5,            # wymagane, 1..5
      "comment": "Świetna!"   # opcjonalne
    }
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
