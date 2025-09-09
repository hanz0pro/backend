from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.game_model import Game
from app.models.wish_list import WishList  # dostosuj import do swojej struktury
from . import api


@api.route("/wishlist/<int:game_id>", methods=["POST"])
@jwt_required()
def add_to_wishlist(game_id):
    user_id = get_jwt_identity()

    # Sprawdź czy gra istnieje
    game = Game.query.get(game_id)
    if not game:
        return jsonify({"message": "Gra nie istnieje."}), 404

    # Czy już jest na wishliście?
    existing = WishList.query.filter_by(user_id=user_id, game_id=game_id).first()
    if existing:
        return jsonify({"message": "Gra już jest na Twojej wishliście."}), 200

    # Dodaj
    wl = WishList(user_id=user_id, game_id=game_id)
    db.session.add(wl)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({"message": "Nie udało się dodać do wishlisty."}), 500

    return jsonify({
        "message": "Dodano do wishlisty.",
        "item": {
            "id": wl.id,
            "game_id": wl.game_id,
            "user_id": wl.user_id
        }
    }), 201



@api.route("/users/me/wishlist", methods=["GET"])
@jwt_required()
def get_my_wishlist():
    user_id = get_jwt_identity()
    items = (
        db.session.query(WishList, Game)
        .join(Game, WishList.game_id == Game.id)
        .filter(WishList.user_id == user_id)
        .all()
    )
    data = [
        {
            "wishlist_item_id": wl.id,
            "game_id": g.id,
            "title": g.title,
            "description": g.description,
            "price": g.price,
            "discount": getattr(g, "discount", 0) or 0,
            "image_path": g.image_path,
            "genres": [x.name for x in g.genres],
            "tags": [x.name for x in g.tags],
        }
        for wl, g in items
    ]
    return jsonify(data), 200