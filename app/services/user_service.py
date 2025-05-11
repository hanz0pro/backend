from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app import db
from app.models import User

def register_user(data):
    if User.query.filter_by(username=data['username']).first():
        return {"msg": "User already exists"}, 409

    hashed_pw = generate_password_hash(data['password'])
    user = User(username=data['username'], password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return {"msg": "User created"}, 201

def login_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=str(user.id))
        return {"access_token": token}, 200

    return {"msg": "Invalid credentials"}, 401
