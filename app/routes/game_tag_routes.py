from flask import Blueprint, request, jsonify
from app import db
from app.models.game_tag_model import Tag
from app.routes import tag_bp


# Dodaj nowy tag
@tag_bp.route("", methods=["POST"])
def create_tag():
    """
    Endpoint tworzenia nowego taga.

    Request JSON:
        {
            "name": "string"   # wymagane, unikalna nazwa taga (np. "Multiplayer", "Open World")
        }

    Response (201 Created):
        {
            "id": 1,
            "name": "Multiplayer"
        }

    Response (400 Bad Request):
        {
            "error": "Tag name is required"
        }

    Response (409 Conflict):
        {
            "error": "Tag already exists"
        }

    Returns:
        tuple: JSON response z utworzonym tagiem lub błąd.
    """
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Tag name is required"}), 400

    existing = Tag.query.filter_by(name=name).first()
    if existing:
        return jsonify({"error": "Tag already exists"}), 409

    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return jsonify({"id": tag.id, "name": tag.name}), 201


# Pobierz wszystkie tagi
@tag_bp.route("", methods=["GET"])
def get_tags():
    """
    Endpoint pobierania wszystkich tagów.

    Request:
        Brak parametrów.

    Response (200 OK):
        [
            {"id": 1, "name": "Multiplayer"},
            {"id": 2, "name": "Open World"},
            {"id": 3, "name": "Singleplayer"}
        ]

    Returns:
        list: Lista tagów w formacie JSON.
    """
    tags = Tag.query.all()
    return jsonify([{"id": tag.id, "name": tag.name} for tag in tags])
