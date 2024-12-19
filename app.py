from pathlib import Path

from flask import Flask
from flask_migrate import Migrate

from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie

migrate = Migrate()

db_path = Path(__file__).parent / "instance" / "moviwebapp.db"

app = Flask(__name__)

data_manager = SQLiteDataManager(str(db_path))

app.config[
    "SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{db_path}")


@app.route('/')
def home():
    movie = Movie()
    movie.id = 1
    movie.user_id = 1
    movie.name = "Jaja"
    movie.director = "Jaja"
    movie.year = 2029
    movie.rating = 10.0

    data_manager.delete_movies(2)

    return "Welcome to MovieWeb App!"


if __name__ == '__main__':
    app.run(debug=True)
