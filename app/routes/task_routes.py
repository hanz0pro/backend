from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import api

from app.services.task_service import get_user_tasks, create_task_for_user

@api.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = get_user_tasks(user_id)
    return jsonify(tasks), 200

@api.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.json
    response, status = create_task_for_user(user_id, data)
    return jsonify(response), status
