from website import create_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# Password
load_dotenv()
db_pw = os.getenv('DB_PASSWORD')

# Create Flask Instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

# Init Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{db_pw}@localhost/CineArchive'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import the Kaggle Dataset
df = pd.read_csv('final_dataset.csv')