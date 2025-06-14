import os

from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename

from app import db
from app.models.game_genre_model import Genre
from app.models.game_model import Game
from app.models.game_tag_model import Tag
from app.routes import game_bp, api


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


UPLOAD_FOLDER = 'static/images/games'  # lub inna ścieżka
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@api.route('games', methods=['POST'])
def create_game():
    title = request.form.get('title')
    description = request.form.get('description')
    price = request.form.get('price')
    genres = request.form.getlist('genres')  # wiele wartości np. ['Action', 'RPG']
    tags = request.form.getlist('tags')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    # Obsługa pliku
    image = request.files.get('image')
    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        image_path = filepath  # względna ścieżka do pliku

    game = Game(
        title=title,
        description=description,
        price=price,
        image_path=image_path
    )

    # Przypisz gatunki
    for name in genres:
        genre = Genre.query.filter_by(name=name).first()
        if genre:
            game.genres.append(genre)

    # Przypisz tagi
    for name in tags:
        tag = Tag.query.filter_by(name=name).first()
        if tag:
            game.tags.append(tag)

    db.session.add(game)
    db.session.commit()
    return jsonify(game_to_dict(game)), 201
# 🔸 Pobierz wszystkie gry
@api.route('games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([game_to_dict(game) for game in games])

# 🔸 Pobierz grę po ID
@api.route('games/<int:game_id>', methods=['GET'])
def get_game(game_id):
    game = Game.query.get_or_404(game_id)
    return jsonify(game_to_dict(game))

#Dodatkowy endpoint
@api.route('games/<int:game_id>/image', methods=['GET'])
def get_game_image(game_id):
    import os
    import mimetypes

    game = Game.query.get_or_404(game_id)

    if not game.image_path:
        return {'error': 'Image not found'}, 404

    backend_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # folder backend/

    full_path = os.path.join(backend_root, game.image_path)


    normalized_full_path = full_path.replace('\\', '/')

    print("Full path:", normalized_full_path)
    if not os.path.isfile(normalized_full_path):
        return {'error': 'File not found on disk'}, 404

    mimetype = mimetypes.guess_type(normalized_full_path)[0] or 'application/octet-stream'
    return send_file(normalized_full_path, mimetype=mimetype)
