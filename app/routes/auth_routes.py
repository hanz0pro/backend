from flask import request, jsonify
from . import api
from app.services.user_service import register_user, login_user

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    response, status = register_user(data)
    return jsonify(response), status

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    response, status = login_user(data)
    return jsonify(response), status
