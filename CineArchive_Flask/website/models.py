from . import db
from flask_login import UserMixin

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.VARCHAR(100), primary_key=True)  # should match the 'id' in the CSV
    title = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)

    directors = db.Column(db.JSON) 
    writers = db.Column(db.JSON)
    stars = db.Column(db.JSON)
    genres = db.Column(db.JSON)
    production_companies = db.Column(db.JSON)
    release_date = db.Column(db.Integer)

    duration = db.Column(db.Integer)  # optional but useful
    rating = db.Column(db.Float)      # optional, e.g. IMDb rating
    languages = db.Column(db.JSON)    # optional

    def __repr__(self):
        return f"<Movie {self.title} ({self.year})>"

class Watchlist(db.Model):
    __tablename__ = 'watchlist'

    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, nullable=False)  # Currently static, but ready for future multi-user support
    movie_id = db.Column(db.VARCHAR(100), db.ForeignKey('movies.id'))
    
    added_at = db.Column(db.DateTime, server_default=db.func.now())  # Optional timestamp for sorting/filtering

    movie = db.relationship('Movie', backref='watchlist_entries')

    def __repr__(self):
        return f"<Watchlist user={self.user_id} movie_id={self.movie_id}>"
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
