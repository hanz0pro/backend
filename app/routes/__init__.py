from flask import Blueprint


game_bp = Blueprint('game_bp', __name__)
api = Blueprint('api', __name__)
genre_bp = Blueprint('genre_bp', __name__)
tag_bp = Blueprint('tag_bp', __name__)

# Importuj i rejestruj wszystkie podmoduły (ręcznie)
from .auth_routes import *
from .task_routes import *
from .util_routes import *
from .game_routes import *
from .game_tag_routes import *
from .game_genre_routes import *
