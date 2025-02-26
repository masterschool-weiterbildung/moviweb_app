from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    relationship
"""
Database models for the MovieWebApp.

This module defines the SQLAlchemy models for the application, including:
- User: Represents a user with a list of favorite movies.
- Movie: Represents a movie with details such as director, year, and rating.

"""

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    """
    Represents a user in the application.

    Attributes:
        id (int): The unique identifier for the user.
        name (str): The name of the user.
        movies (list[Movie]): List of movies associated with the user.

    Methods:
        __repr__: Provides a developer-friendly string representation of the object.
        __str__: Provides a user-friendly string representation of the object.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    movies = relationship('Movie', backref='User',
                          cascade='all, delete')

    def __repr__(self):
        return (f"User(id = {self.id}, "
                f"name = {self.name})"
                )

    def __str__(self):
        return (f"User(id = {self.id}, "
                f"name = {self.name})"
                )


class Movie(db.Model):
    """
    Represents a movie in the application.

    Attributes:
        id (int): The unique identifier for the movie.
        user_id (int): The ID of the associated user.
        name (str): The title of the movie.
        director (str): The name of the movie's director.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.

    Methods:
        __repr__: Provides a developer-friendly string representation of the object.
        __str__: Provides a user-friendly string representation of the object.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(unique=False)
    director: Mapped[str]
    year: Mapped[int]
    rating: Mapped[float]
    path: Mapped[str]

    def __repr__(self):
        return (f"Movie(id = {self.id}, "
                f"name = {self.name}, "
                f"director = {self.director}, "
                f"year = {self.year}, "
                f"rating = {self.rating})"
                )

    def __str__(self):
        return (f"Movie(id = {self.id}, "
                f"name = {self.name}, "
                f"director = {self.director}, "
                f"year = {self.year}, "
                f"rating = {self.rating})"
                )
