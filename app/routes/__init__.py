from flask import Blueprint

api = Blueprint('api', __name__)

# Importuj i rejestruj wszystkie podmoduły (ręcznie)
from .auth_routes import *
from .task_routes import *
from .util_routes import *
