import logging

from flask import Blueprint, request, jsonify
from .models import User, Task, Category
from . import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash

api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"}), 200

@api.route('/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        print("Incoming data:", data)
        return jsonify({"msg": "User already exists"}), 409
    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@api.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Invalid credentials"}), 401

@api.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    from flask_jwt_extended import get_jwt_identity
    from .models import Task

    user_id = get_jwt_identity()
    print("✅ Zadania dla user_id:", user_id)

    tasks = Task.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            'id': task.id,
            'title': task.title,
            'done': task.done,
            'category': task.category.name if task.category else None
        }
        for task in tasks
    ])


@api.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.json
    task = Task(title=data['title'], user_id=user_id, category_id=data.get('category_id'))
    db.session.add(task)
    db.session.commit()
    return jsonify({"msg": "Task created"}), 201

# /api/health - prosty healthcheck
@api.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# /api/db-check - testowe zapytanie do bazy
@api.route('/db-check', methods=['GET'])
def db_check():
    try:
        # np. policz użytkowników
        count = User.query.count()
        return jsonify({"db": "ok", "users": count}), 200
    except Exception as e:
        return jsonify({"db": "error", "details": str(e)}), 500

@api.route('/debug-token', methods=['GET'])
def debug_token():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        print("Headers:", dict(request.headers))
        return jsonify({"msg": "Token OK", "user_id": user_id}), 200
    except Exception as e:
        print("Token error:", str(e))
        return jsonify({"msg": "Token ERROR", "details": str(e)}), 422