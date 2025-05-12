from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, jsonify
from flask_login import current_user, login_required
from . import db
from sqlalchemy import func, text
import ast
import re

views = Blueprint('views', __name__)

def clean_string(input_str):
    cleaned_str = re.sub(r'[\[\]"\'\s]+', ' ', input_str)
    cleaned_str = re.sub(r'\s*,\s*', ', ', cleaned_str)
    cleaned_str = re.sub(r',\s*,+', ',', cleaned_str)
    cleaned_str = re.sub(r'\s+', ' ', cleaned_str)
    return cleaned_str.strip()

@views.before_app_request
def check_db_connection():
    try:
        result = db.session.execute(text('SELECT 1'))
        db.session.commit()  # This is a simple test query
        current_app.logger.info("Database connection is successful")
    except Exception as e:
        current_app.logger.error(f"Error connecting to database: {e}")

@views.route('/home')
def home():
    return render_template('home.html')

@views.route('/')
def index():
    return redirect(url_for('home'))

# Route to handle search logic and return JSON
@views.route('/search')
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])

    try:
        stmt = text("CALL search_movies(:query_text)")
        results = db.session.execute(stmt, {'query_text': query.lower()}).mappings().fetchall()
        movies = [dict(row) for row in results]
        return jsonify(movies)
    except Exception as e:
        current_app.logger.error(f"Error in search_movies: {e}")
        return jsonify([]), 500

@views.route('/watchlist')
@login_required
def view_watchlist():
    try:
        stmt = text("CALL get_watchlist_movies(:uid)")
        result = db.session.execute(stmt, {'uid': current_user.id})
        row = result.fetchall()

        def parse_movie_row(row):
            return {
                "id": row[0],
                "title": row[1],
                "year": row[2],
                "description": row[3],
                "directors": clean_string(row[4]),
                "genres": ast.literal_eval(row[5]),
                "rating": row[6],
                "runtime": row[8],
                "languages": ast.literal_eval(row[9]),
                "actors": ast.literal_eval(row[10]),
                "writers": ast.literal_eval(row[11]),
                "production_companies": ast.literal_eval(row[12])
            }

        movies = [parse_movie_row(row) for row in row]

    except Exception as e:
        current_app.logger.error(f"Error fetching watchlist: {e}")
        return render_template("watchlist.html", movies=[])
    
    return render_template("watchlist.html", movies=movies)

@views.route('/watchlist/add/<string:movie_id>', methods=['POST'])
def add_to_watchlist(movie_id):
    try:
        stmt = text("CALL add_to_watchlist(:uid, :mid)")
        db.session.execute(stmt, {'uid': current_user.id, 'mid': str(movie_id)})
        db.session.commit()
        flash('Movie added to watchlist!', 'success')
    except Exception as e:
        current_app.logger.error(f"Error adding to watchlist: {e}")
        flash('Failed to add movie to watchlist.', 'error')
    return redirect(url_for('views.view_watchlist'))

@views.route('/watchlist/remove/<string:movie_id>', methods=['POST'])
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
    stars = request.args.get('stars')
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

    return render_template('movie.html', movies=movies, title=title, directors=directors, year=year)

# View full movie details - poster (using api), title, director, release date
@views.route('/movie/<string:movie_id>')
def movie_details(movie_id):
    try:
        stmt = text("CALL get_movie_details(:movie_id_param)")
        result = db.session.execute(stmt, {'movie_id_param': movie_id})
        movie = result.mappings().fetchone()  # Single row as dict
        if not movie:
            return render_template('404.html'), 404
        
        movie = dict(movie)

        movie['directors'] = clean_string(str(movie['directors']))
        movie['writers'] = clean_string(str(movie['writers']))
        movie['stars'] = clean_string(str(movie['stars']))
        movie['genres'] = clean_string(str(movie['genres']))
        movie['production_companies'] = clean_string(str(movie['production_companies']))
        movie['languages'] = clean_string(str(movie['languages']))

    except Exception as e:
        current_app.logger.error(f"Error fetching movie details: {e}")
        return render_template('500.html'), 500

    return render_template('movie.html', movie=movie)

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