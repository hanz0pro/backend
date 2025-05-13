from flask import Blueprint, request, jsonify
from app import db
from app.models.game_genre_model import Genre
from app.routes import genre_bp


# Dodaj nowy gatunek
@genre_bp.route('', methods=['POST'])
def create_genre():
    data = request.json
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Genre name is required'}), 400

    existing = Genre.query.filter_by(name=name).first()
    if existing:
        return jsonify({'error': 'Genre already exists'}), 409

    genre = Genre(name=name)
    db.session.add(genre)
    db.session.commit()
    return jsonify({'id': genre.id, 'name': genre.name}), 201

# Pobierz wszystkie gatunki
@genre_bp.route('', methods=['GET'])
def get_genres():
    genres = Genre.query.all()
    return jsonify([{'id': genre.id, 'name': genre.name} for genre in genres])
