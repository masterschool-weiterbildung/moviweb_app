"""
MovieWebApp: A Flask-based web application for managing users and their favorite movies.

Modules and Libraries Used:
- pathlib
- flask
- flask_migrate
- SQLiteDataManager
- models

Application Configuration:
- Database: SQLite database located at `instance/moviwebapp.db`.

"""

from pathlib import Path

from flask import request, render_template, Flask, redirect, url_for, abort

from flask_migrate import Migrate

from datamanager.sqlite_data_manager import SQLiteDataManager
from models import User, Movie
from marshmallow import Schema, fields, validate, ValidationError

migrate = Migrate()

db_path = Path(__file__).parent / "instance" / "moviwebapp.db"

app = Flask(__name__)

data_manager = SQLiteDataManager(str(db_path))

app.config[
    "SQLALCHEMY_DATABASE_URI"] = (f"sqlite:///{db_path}")


class MovieSchemaUpdate(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1,
                                                              error="Name cannot be blank"))

    director = fields.Str(required=True, validate=validate.Length(min=1,
                                                                  error="director cannot be blank"))
    year = fields.Str(required=True, validate=validate.Length(min=1,
                                                              error="year cannot be blank"))
    rating = fields.Str(required=True, validate=validate.Length(min=1,
                                                                error="rating cannot be blank"))

    id = fields.Str(required=True, validate=validate.Length(min=1,
                                                            error="rating cannot be blank"))


class UserMovieSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1,
                                                              error="Name cannot be blank"))


movie_schema_update = MovieSchemaUpdate()
user_movie_schema = UserMovieSchema()


@app.route('/')
def index():
    """
    Renders the home page.

    Returns:
        str: Rendered `index.html` template.
    """
    return render_template('index.html')


@app.route('/users')
def list_users():
    """
    Lists all users.

    Returns:
        str: Rendered `users.html` template with user data.
        500: Error page if data retrieval fails.
    """
    try:
        users = data_manager.get_all_users()
    except IOError as e:
        return "Error getting all users", 500

    return render_template('users.html', users=users)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_users_favorite_movies(user_id: int):
    """
    Displays a user's favorite movies.

    Parameter:
        user_id (int): ID of the user.

    Returns:
        str: Rendered `user-movies.html` template with user movie data.
        404: If user or movies are not found.
        500: If data retrieval fails.
    """
    try:
        result = data_manager.get_user_movies(user_id)

        if not result:
            return show_all_users("False")

        return render_template('user-movies.html', result=result,
                               username=result[0].name)
    except IOError as e:
        abort(500)
    except IndexError as e:
        abort(500)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Adds a new user.

    Returns:
        str: Rendered `add-user.html` template for GET request.
        Redirect: Redirects to user list on successful POST.
        500: If user addition fails.
    """
    if request.method == 'POST':
        try:
            result = user_movie_schema.load(request.form)
            name = result['name']

            user = User()
            user.name = name

            data_manager.add_user(user)

        except IOError as e:
            return show_all_users("add_user")
        except ValidationError as ve:
            return show_all_users("add_user_blank")

        return show_all_users("add_user_success")

    return render_template('add-user.html')


def show_all_users(message: str):
    try:
        users = data_manager.get_all_users()
    except IOError as e:
        return "Error getting all users", 500
    return render_template('users.html',
                           users=users,
                           message=message)


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id: int):
    """
    Adds a movie to a user's favorite list.

    Parameter:
        user_id (int): ID of the user.

    Returns:
        str: Rendered `add-movie.html` template for GET request.
        Redirect: Redirects to home page on successful POST.
        500: If movie addition fails.
    """
    if request.method == 'POST':
        result = user_movie_schema.load(request.form)
        name = result['name']

        try:
            movie = data_manager.get_user_from_api(name)
        except IOError as e:
            # return show_all_users("no_exist_movie")
            print(e)
        except Exception as e:
            # return show_all_users("no_exist_movie")
            print(e)

        movie.user_id = user_id
        movie.name = name

        try:
            data_manager.add_movie(movie)
            return redirect(
                url_for('get_users_favorite_movies', user_id=user_id))
        except IOError as e:
            return show_all_users("False")
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
    """
     Updates a movie's details.

     Parameters:
         user_id (int): ID of the user.
         movie_id (int): ID of the movie.

     Returns:
         str: Rendered `update-movie.html` template for GET request.
         Redirect: Redirects to home page on successful POST.
         500: If movie update fails.
     """
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

        return redirect(url_for('get_users_favorite_movies', user_id=user_id))

    try:
        return_movie = data_manager.get_movie(movie_id)
    except IOError as e:
        abort(500)

    return render_template('update-movie.html', movie=return_movie,
                           user_id=user_id)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete(user_id: int, movie_id: int):
    """
    Deletes a movie from a user's favorite list.

    Parameters:
        user_id (int): ID of the user.
        movie_id (int): ID of the movie.

    Returns:
        Redirect: Redirects to user list on successful deletion.
        500: If movie deletion fails.
    """
    try:
        data_manager.delete_movies(movie_id)
    except IOError as e:
        abort(500)

    return redirect(
        url_for('get_users_favorite_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(error):
    """
    Renders a custom 404 error page.

    Parameter:
        error: The error that caused the handler to be invoked.

    Returns:
        Tuple[str, int]: Rendered `404.html` template and status code 404.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(error):
    """
    Renders a custom 500 error page.

    Parameter:
        error: The error that caused the handler to be invoked.

    Returns:
        Tuple[str, int]: Rendered `500.html` template and status code 500.
    """
    return render_template('500.html'), 500


if __name__ == '__main__':
    """
    Runs the Flask application.

    The application is hosted on `0.0.0.0:5000` with debug mode enabled.
    """
    app.run(host="0.0.0.0", port=5000, debug=True)
