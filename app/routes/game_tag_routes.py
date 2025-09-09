from flask import Blueprint, request, jsonify
from app import db
from app.models.game_tag_model import Tag
from app.routes import tag_bp


# Dodaj nowy tag
@tag_bp.route("", methods=["POST"])
def create_tag():
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
    tags = Tag.query.all()
    return jsonify([{"id": tag.id, "name": tag.name} for tag in tags])
