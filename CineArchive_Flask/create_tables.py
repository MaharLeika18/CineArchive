from website import db, create_app  
from website.models import Movie 
from website import db
from website.models import Movie
import ast

#app = create_app()

#with app.app_context():
#    db.create_all()

def convert_stringified_fields():
    fields_to_convert = ['directors', 'writers', 'stars', 'genres', 'production_companies']

    movies = Movie.query.all()
    updated_count = 0

    for movie in movies:
        changed = False
        for field in fields_to_convert:
            value = getattr(movie, field)
            if isinstance(value, str):
                try:
                    parsed = ast.literal_eval(value)
                    if isinstance(parsed, list):
                        setattr(movie, field, parsed)
                        changed = True
                except (ValueError, SyntaxError):
                    print(f"Skipping movie ID {movie.id}, invalid list string in field '{field}': {value}")
        if changed:
            updated_count += 1

    db.session.commit()
    print(f"Updated {updated_count} movie records.")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        convert_stringified_fields()


# This is just a dev file im using to test the backend
# To be deleted when all is done