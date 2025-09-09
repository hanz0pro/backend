from flask import request, jsonify

from app import db
from app.models.game_genre_model import Genre
from app.routes import genre_bp, api


# Dodaj nowy gatunek
@api.route("genre", methods=["POST"])
def create_genre():
    """
    Endpoint dodawania nowego gatunku gier.

    Request JSON:
        {
            "name": "string"   # wymagane, unikalna nazwa gatunku (np. "RPG", "Action")
        }

    Response (201 Created):
        {
            "id": 1,
            "name": "RPG"
        }

    Response (400 Bad Request):
        {
            "error": "Genre name is required"
        }

    Response (409 Conflict):
        {
            "error": "Genre already exists"
        }

    Returns:
        tuple: JSON response z utworzonym gatunkiem lub błąd.
    """
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Genre name is required"}), 400

    existing = Genre.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Genre already exists"}), 409

    genre = Genre(name=name)
    db.session.add(genre)
    db.session.commit()
    return jsonify({"id": genre.id, "name": genre.name}), 201


# Pobierz wszystkie gatunki
@api.route("genre", methods=["GET"])
def get_genres():
    """
    Endpoint pobierania wszystkich gatunków gier.

    Request:
        Brak parametrów.

    Response (200 OK):
        [
            {"id": 1, "name": "RPG"},
            {"id": 2, "name": "Action"},
            {"id": 3, "name": "Strategy"}
        ]

    Returns:
        list: Lista gatunków w formacie JSON.
    """
    genres = Genre.query.all()
    return jsonify([{"id": genre.id, "name": genre.name} for genre in genres])
