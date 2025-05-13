from multiprocessing import AuthenticationError

from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException, BadRequest, NotFound, MethodNotAllowed, InternalServerError, Unauthorized

error_bp = Blueprint('error_bp', __name__)

# Obsługa znanych błędów HTTP
@error_bp.app_errorhandler(BadRequest)
def handle_400(error):
    return jsonify(error="Bad Request", message=str(error)), 400

@error_bp.app_errorhandler(NotFound)
def handle_404(error):
    return jsonify(error="Not Found", message=str(error)), 404

@error_bp.app_errorhandler(Unauthorized)
def handle_401(error):
    return jsonify(error="Unauthorized", message=str(error)), 401

@error_bp.app_errorhandler(MethodNotAllowed)
def handle_405(error):
    return jsonify(error="Method Not Allowed", message=str(error)), 405

@error_bp.app_errorhandler(InternalServerError)
def handle_500(error):
    return jsonify(error="Internal Server Error", message="Coś poszło nie tak."), 500

# Obsługa wszystkich innych wyjątków
@error_bp.app_errorhandler(Exception)
def handle_exception(error):
    return jsonify(error="Unexpected Error", message=str(error)), 500
