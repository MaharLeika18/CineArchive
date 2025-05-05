from flask import Blueprint, render_template, request, redirect, url_for
from .models import Movie, Watchlist
from . import db
from sqlalchemy import or_
from flask_login import current_user
from sqlalchemy import func
from flask import current_app
from sqlalchemy import text

views = Blueprint('views', __name__)

@views.before_app_request
def check_db_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        db.session.commit()  # This is a simple test query
        current_app.logger.info("Database connection is successful")
    except Exception as e:
        current_app.logger.error(f"Error connecting to database: {e}")

@views.route('/')
def home():
    return "<h1>Test</h1>"  # Change this into the home template

@views.route('/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    if query:
        try:
            results = Movie.query.filter(
                or_(
                    func.lower(Movie.title).ilike(f"%{query}%"),
                    func.lower(Movie.description).ilike(f"%{query}%"),
                    func.lower(Movie.directors).ilike(f"%{query}%"),
                    func.lower(Movie.writers).ilike(f"%{query}%"),
                    func.lower(Movie.stars).ilike(f"%{query}%"),
                    func.lower(Movie.genres).ilike(f"%{query}%"),
                    func.lower(Movie.production_companies).ilike(f"%{query}%"),
                )
            ).all()
            current_app.logger.info(f"Query successful: {query}, Found {len(results)} results")
        except Exception as e:
            current_app.logger.error(f"Error in search query: {e}")
    else:
        current_app.logger.info("Empty query received.")

    return render_template('search.html', results=results, query=query)

@views.route('/watchlist')
def view_watchlist():
    watchlist_items = Watchlist.query.filter_by(user_id = current_user.id).all()
    movie_ids = [item.movie_id for item in watchlist_items]
    movies = Movie.query.filter(Movie.id.in_(movie_ids)).all()
    return render_template('watchlist.html', movies=movies)

@views.route('/watchlist/add/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    if not Watchlist.query.filter_by(user_id = current_user.id, movie_id=movie_id).first():
        db.session.add(Watchlist(user_id = current_user.id, movie_id=movie_id))
        db.session.commit()
    return redirect(url_for('views.view_watchlist'))

@views.route('/watchlist/remove/<int:movie_id>', methods=['POST'])
def remove_from_watchlist(movie_id):
    Watchlist.query.filter_by(user_id = current_user.id, movie_id=movie_id).delete()
    db.session.commit()
    return redirect(url_for('views.view_watchlist'))