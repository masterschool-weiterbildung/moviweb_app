from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    relationship


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
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
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(unique=True)
    director: Mapped[str]
    year: Mapped[int]
    rating: Mapped[float]

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
