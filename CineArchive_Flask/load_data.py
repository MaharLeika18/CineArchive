import pandas as pd
from website import create_app, db
from website.models import Movie
import ast
import csv

def clean_release_date(value):
    if not value or value.strip() == '':
        return None
    try:
        return int(float(value))
    except ValueError:
        return None
    
def load_csv_to_db(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(f"Processing movie: {row['title']}")  # Debugging line
            release_date = clean_release_date(row['release_date'])
            movie = Movie(
                id=row['id'],
                title=row['title'],
                year=int(row['year']) if row['year'] else None,
                description=row['description'],
                directors=(row['directors']),
                writers=(row['writers']),
                stars=(row['stars']),
                genres=(row['genres']),
                production_companies=(row['production_companies']),
                release_date=release_date,
                duration=row['duration'],
                rating=float(row['rating']) if row['rating'] else None,
                languages=(row['languages']),
            )

            # Insert to DB if it doesn't exist
            if not db.session.get(Movie, movie.id):
                db.session.add(movie)

        db.session.commit()

app = create_app()

with app.app_context():
    csv_path = 'CineArchive_Flask/data/final_dataset.csv'
    db.session.query(Movie).delete()
    db.session.commit()
    load_csv_to_db(csv_path)
    print("Database loaded successfully.")
