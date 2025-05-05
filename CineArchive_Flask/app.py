from website import db, create_app
from flask_migrate import Migrate
from flask.cli import FlaskGroup
from website.models import Movie

# Create Flask Instance
app = create_app()
migrate = Migrate(app, db)
cli = FlaskGroup(app)

if __name__ == '__main__':
    app.run(debug=True)
    cli()



