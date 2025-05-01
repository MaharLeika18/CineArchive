import pandas as pd
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# DB credentials from .env
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Read the cleaned CSV
df = pd.read_csv('data/movies_cleaned.csv')

# Optional: preview first rows
print("Preview of dataset:")
print(df.head())

# Connect to MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# TODO: REWRITE THE FF TO MAKE THE DATA MATCH WITH THE MOVIES DATASET

# Insert data into the `movies` table
insert_query = """
INSERT INTO movies (title, genre, release_year, rating, runtime, language, director)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (
        row['title'],
        row['genre'],
        int(row['release_year']),
        float(row['rating']) if not pd.isna(row['rating']) else None,
        int(row['runtime']) if not pd.isna(row['runtime']) else None,
        row['language'],
        row['director']
    ))

conn.commit()
print("✅ Data imported successfully.")

# Clean up
cursor.close()
conn.close()
