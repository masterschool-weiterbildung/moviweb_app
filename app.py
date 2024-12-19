from pathlib import Path

from flask import Flask, render_template
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
def index():
    movie = Movie()
    movie.id = 1
    movie.user_id = 1
    movie.name = "Jaja"
    movie.director = "Jaja"
    movie.year = 2029
    movie.rating = 10.0

    data_manager.delete_movies(2)

    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()

    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_users_favorite_movies(user_id: int):
    pass


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    pass


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id: int):
    pass


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
           methods=['GET', 'POST'])
def update_movie(user_id: int, movie_id: int):
    pass


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete(user_id: int, movie_id: int):
    pass


if __name__ == '__main__':
    app.run(debug=True)
