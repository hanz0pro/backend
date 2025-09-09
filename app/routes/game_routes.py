import json
import os

from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename

from app import db
from app.models.game_genre_model import Genre
from app.models.game_model import Game
from app.models.game_tag_model import Tag
from app.routes import api


# 🔹 Pomocnicze: konwersja do JSON
def game_to_dict(game):
    """
    Konwertuje obiekt `Game` do słownika JSON-owalnego.

    Args:
        game (Game): Instancja gry.

    Returns:
        dict: Słownik zawierający kluczowe informacje o grze:
            - id (int)
            - title (str)
            - description (str|None)
            - price (float|None)
            - image_path (str|None)
            - genres (list[str])
            - tags (list[str])
            - discount (float|None)
    """
    return {
        "id": game.id,
        "title": game.title,
        "description": game.description,
        "price": game.price,
        "image_path": game.image_path,
        "genres": [genre.name for genre in game.genres],
        "tags": [tag.name for tag in game.tags],
        "discount": game.discount,
    }


UPLOAD_FOLDER = "static/images/games"  # lub inna ścieżka
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    """
    Sprawdza, czy przesłany plik ma dozwolone rozszerzenie.

    Args:
        filename (str): Nazwa pliku.

    Returns:
        bool: True jeśli rozszerzenie jest dozwolone, w przeciwnym razie False.
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_list(field: str) -> list[str]:
    """
    Pobiera listę wartości z multipart/form-data.

    Obsługuje dwa warianty:
      1) Powtarzane klucze (np. genres=RPG & genres=Action)
      2) Jedno pole będące JSON-ową tablicą (np. genres='["RPG","Action"]')
      3) Alternatywną składnię `field[]`

    Args:
        field (str): Nazwa pola formularza (np. "genres", "tags").

    Returns:
        list[str]: Lista wartości (może być pusta).
    """
    vals = request.form.getlist(field)
    if len(vals) == 1:
        v = vals[0]
        try:
            parsed = json.loads(v)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass
    # alternatywny zapis z nawiasami: genres[]
    vals_alt = request.form.getlist(f"{field}[]")
    return vals or vals_alt or []


def to_float(val, default=None):
    """
    Bezpiecznie konwertuje wartość tekstową na float.

    Zamienia przecinki na kropki. W przypadku błędu zwraca `default`.

    Args:
        val (str|None): Wartość wejściowa (np. "199.99" lub "199,99").
        default (float|None): Wartość domyślna przy błędzie.

    Returns:
        float|None: Liczba zmiennoprzecinkowa lub `default`.
    """
    if val in (None, ""):
        return default
    try:
        return float(str(val).replace(",", "."))
    except ValueError:
        return default


@api.route("games", methods=["POST"])
def create_game():
    """
    Tworzy nową grę.

    Request:
        Content-Type: multipart/form-data
        Pola formularza:
            - title (str, required)
            - description (str, optional)
            - price (str/float, optional)  # liczba jako tekst
            - discount (str/float, optional, 0..100)  # procent
            - genres (list[str] lub JSON array, optional)
            - tags (list[str] lub JSON array, optional)
            - image (file, optional)  # png/jpg/jpeg/gif

    Response (201 Created):
        JSON z danymi nowej gry (patrz `game_to_dict`).

    Response (400 Bad Request):
        {"error": "Title is required"}

    Uwagi:
        - Gatunki i tagi są dopinane tylko, jeśli istnieją w bazie (case-insensitive).
        - `discount` poza zakresem [0, 100] zostanie ustawiony na 0.0.
        - `image_path` przechowuje ścieżkę względną do statycznego pliku.
    """
    title = request.form.get("title")
    description = request.form.get("description")
    price_raw = request.form.get("price")
    genres_in = parse_list("genres")
    tags_in = parse_list("tags")
    discount_raw = request.form.get("discount")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    discount = to_float(discount_raw, default=0.0)
    if discount is None or discount < 0 or discount > 100:
        discount = 0.0

    # plik
    image = request.files.get("image")
    image_path = None
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)
        # lepiej zapisać ścieżkę webową z forward slashem:
        image_path = f"static/images/games/{filename}"

    # cena -> float
    price = float(price_raw) if price_raw not in (None, "") else None

    game = Game(
        title=title,
        description=description,
        price=price,
        image_path=image_path,
        discount=discount,
    )
    db.session.add(game)
    db.session.flush()

    # dopasowanie po nazwie (case-insensitive)
    for name in genres_in:
        g = Genre.query.filter(Genre.name.ilike(name)).first()
        if g:
            game.genres.append(g)

    for name in tags_in:
        t = Tag.query.filter(Tag.name.ilike(name)).first()
        if t:
            game.tags.append(t)

    db.session.commit()
    return jsonify(game_to_dict(game)), 201


# 🔸 Pobierz wszystkie gry
@api.route("games", methods=["GET"])
def get_games():
    """
    Zwraca listę wszystkich gier.

    Request:
        Brak parametrów.

    Response (200 OK):
        [
          { ...game_to_dict... },
          ...
        ]
    """
    games = Game.query.all()
    return jsonify([game_to_dict(game) for game in games])


# 🔸 Pobierz grę po ID
@api.route("games/<int:game_id>", methods=["GET"])
def get_game(game_id):
    """
    Zwraca szczegóły gry o podanym `game_id`.

    Args:
        game_id (int): ID gry.

    Response (200 OK):
        { ...game_to_dict... }

    Response (404 Not Found):
        {"message": "404 Not Found"}  # domyślna odpowiedź Flask `get_or_404`
    """
    game = Game.query.get_or_404(game_id)
    return jsonify(game_to_dict(game))


# Dodatkowy endpoint
@api.route("games/<int:game_id>/image", methods=["GET"])
def get_game_image(game_id):
    """
    Serwuje plik graficzny okładki gry.

    Args:
        game_id (int): ID gry.

    Response (200 OK):
        Zwraca binarną zawartość pliku z poprawnym `Content-Type`.

    Response (404 Not Found):
        {"error": "Image not found"}           # gdy `image_path` puste
        {"error": "File not found on disk"}    # gdy plik nie istnieje fizycznie

    Uwagi:
        - Ścieżka jest liczona względem katalogu backendu.
        - Dla bezpieczeństwa pliki są serwowane tylko z przewidzianej lokalizacji.
    """
    import os
    import mimetypes

    game = Game.query.get_or_404(game_id)

    if not game.image_path:
        return {"error": "Image not found"}, 404

    backend_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )  # folder backend/

    full_path = os.path.join(backend_root, game.image_path)

    normalized_full_path = full_path.replace("\\", "/")

    print("Full path:", normalized_full_path)
    if not os.path.isfile(normalized_full_path):
        return {"error": "File not found on disk"}, 404

    mimetype = (
        mimetypes.guess_type(normalized_full_path)[0] or "application/octet-stream"
    )
    return send_file(normalized_full_path, mimetype=mimetype)
