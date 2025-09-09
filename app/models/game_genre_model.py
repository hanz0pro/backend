from app import db

game_genre = db.Table(
    "game_genre",
    db.Column("game_id", db.Integer, db.ForeignKey("game.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True),
)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre(name='{self.name}')>"
