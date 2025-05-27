from app import db
from app.models.role_model import user_roles


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True, cascade="all, delete-orphan")
    wishlist = db.relationship('WishList', backref='user', lazy=True, cascade="all, delete-orphan")
    roles = db.relationship('Role', secondary=user_roles, back_populates='users')