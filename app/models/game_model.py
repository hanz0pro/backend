from app import db
from app.models.game_genre_model import game_genre
from app.models.game_tag_model import game_tag


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float)
    discount = db.Column(db.Float)
    image_path = db.Column(db.String(255))

    # wiele gatunków
    genres = db.relationship(
        "Genre", secondary=game_genre, backref=db.backref("games", lazy="dynamic")
    )
    # wiele tagów
    tags = db.relationship(
        "Tag", secondary=game_tag, backref=db.backref("games", lazy="dynamic")
    )

    reviews = db.relationship(
        "Review", backref="game", lazy=True, cascade="all, delete-orphan"
    )
    wishlists = db.relationship(
        "WishList", backref="game", lazy=True, cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Game(title='{self.title}', price={self.price})>"
