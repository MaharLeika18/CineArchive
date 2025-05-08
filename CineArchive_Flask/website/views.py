from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import current_user, login_required
from . import db
from sqlalchemy import func, text

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
    query = request.args.get('q', '')
    results = []

    if query:
        try:
            stmt = text("CALL search_movies(:query_text)")
            result_proxy = db.session.execute(stmt, {'query_text': query})
            results = result_proxy.mappings().all()
        except Exception as e:
            current_app.logger.error(f"Stored procedure error: {e}")

    return render_template('search.html', results=results, query=query)

# View full movie details - poster (using api), title, director, release date
@views.route('/movie/<string:movie_id>')
def movie_details(movie_id):
    try:
        stmt = text("CALL get_movie_details(:movie_id_param)")
        result = db.session.execute(stmt, {'movie_id_param': movie_id})
        movie = result.mappings().fetchone()  # Single row as dict
        if not movie:
            return render_template('404.html'), 404
    except Exception as e:
        current_app.logger.error(f"Error fetching movie details: {e}")
        return render_template('500.html'), 500

    return render_template('movie_details.html', movie=movie)

@views.route('/watchlist')
@login_required
def view_watchlist():
    try:
        stmt = text("CALL get_watchlist_movies(:uid)")
        result = db.session.execute(stmt, {'uid': current_user.id})
        movies = result.fetchall()
    except Exception as e:
        current_app.logger.error(f"Error fetching watchlist: {e}")
        movies = []
    return render_template('watchlist.html', movies=movies)

@views.route('/watchlist/add/<int:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    try:
        stmt = text("CALL add_to_watchlist(:uid, :mid)")
        db.session.execute(stmt, {'uid': current_user.id, 'mid': str(movie_id)})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error adding to watchlist: {e}")
    return redirect(url_for('views.view_watchlist'))

@views.route('/watchlist/remove/<int:movie_id>', methods=['POST'])
def remove_from_watchlist(movie_id):
    try:
        stmt = text("CALL remove_from_watchlist(:uid, :mid)")
        db.session.execute(stmt, {'uid': current_user.id, 'mid': str(movie_id)})
        db.session.commit()
    except Exception as e:
        current_app.logger.error(f"Error removing from watchlist: {e}")
    return redirect(url_for('views.view_watchlist'))

# List all films function + filtering
@views.route('/movie', methods=['GET'])
def list_movies():
    title = request.args.get('title')
    directors = request.args.get('directors')
    year = request.args.get('year', type=int)

    try:
        result = db.session.execute(
            text("CALL list_movies_filtered(:title, :directors, :year)"),
            {"title": title, "directors": directors, "year": year}
        )
        movies = [dict(row._mapping) for row in result.fetchall()]
    except Exception as e:
        current_app.logger.error(f"Error fetching filtered movies: {e}")
        movies = []

    return render_template('movies.html', movies=movies, title=title, directors=directors, year=year)

# Random movie function
@views.route('/random')
def random_movie():
    try:
        stmt = text("CALL get_random_movie()")
        result = db.session.execute(stmt)
        movie = result.mappings().fetchone()
        if not movie:
            return render_template('404notfound.html', message="No movies found."), 404
    except Exception as e:
        current_app.logger.error(f"Error fetching random movie: {e}")
        return render_template('500.html'), 500

    return render_template('movie_details.html', movie=movie)