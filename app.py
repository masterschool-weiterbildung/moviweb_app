from pathlib import Path

from flask import request, render_template, Flask, redirect, url_for, abort

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
    return render_template('index.html')


@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
    except IOError as e:
        return "Error getting all users", 500

    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_users_favorite_movies(user_id: int):
    try:
        result = data_manager.get_user_movies(user_id)

        if not result:
            abort(404)

        return render_template('user-movies.html', result=result,
                               username=result[0].name)
    except IOError as e:
        abort(500)
    except IndexError as e:
        abort(500)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get("name")

        user = User()
        user.name = name

        try:
            data_manager.add_user(user)
        except IOError as e:
            abort(500)

        return redirect(url_for('list_users'))

    return render_template('add-user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id: int):
    if request.method == 'POST':
        name = request.form.get("name")

        try:
            movie = data_manager.get_user_from_api(name)
        except IOError as e:
            abort(500)
        except Exception as e:
            abort(500)

        movie.user_id = user_id
        movie.name = name

        try:
            data_manager.add_movie(movie)
        except IOError as e:
            abort(500)

        return redirect(url_for('index'))
    else:
        try:
            users = data_manager.get_all_users()
        except IOError as e:
            abort(500)

        return render_template('add-movie.html', users=users,
                               user_id=user_id)


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>',
           methods=['GET', 'POST'])
def update_movie(user_id: int, movie_id: int):
    if request.method == 'POST':
        id = request.form.get("id")
        name = request.form.get("name")
        director = request.form.get("director")
        year = request.form.get("year")
        rating = request.form.get("rating")

        movie = Movie()
        movie.id = id
        movie.user_id = user_id
        movie.name = name
        movie.director = director
        movie.year = int(year)
        movie.rating = float(rating)

        try:
            data_manager.update_movie(movie)
        except IOError as e:
            abort(500)

        return redirect(url_for('index'))

    try:
        return_movie = data_manager.get_movie(movie_id)
    except IOError as e:
        abort(500)

    return render_template('update-movie.html', movie=return_movie,
                           user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete(user_id: int, movie_id: int):
    try:
        data_manager.delete_movies(movie_id)
    except IOError as e:
        abort(500)

    return redirect(url_for('list_users'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=False)
