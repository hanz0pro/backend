from flask import Blueprint, request, jsonify
from app import db
from app.models.game_model import Game
from app.models.game_genre_model import Genre
from app.models.game_tag_model import Tag
from app.routes import game_bp


# 🔹 Pomocnicze: konwersja do JSON
def game_to_dict(game):
    return {
        'id': game.id,
        'title': game.title,
        'description': game.description,
        'price': game.price,
        'image_path': game.image_path,
        'genres': [genre.name for genre in game.genres],
        'tags': [tag.name for tag in game.tags]
    }

# 🔸 Dodaj nową grę
@game_bp.route('', methods=['POST'])
def create_game():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    image_path = data.get('image_path')
    genre_names = data.get('genres', [])
    tag_names = data.get('tags', [])

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    game = Game(
        title=title,
        description=description,
        price=price,
        image_path=image_path
    )

    # Przypisz gatunki
    for name in genre_names:
        genre = Genre.query.filter_by(name=name).first()
        if genre:
            game.genres.append(genre)

    # Przypisz tagi
    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        if tag:
            game.tags.append(tag)
    print(game_to_dict(game))
    db.session.add(game)
    db.session.commit()
    return jsonify(game_to_dict(game)), 201

# 🔸 Pobierz wszystkie gry
@game_bp.route('', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([game_to_dict(game) for game in games])

# 🔸 Pobierz grę po ID
@game_bp.route('/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game_to_dict(game))
