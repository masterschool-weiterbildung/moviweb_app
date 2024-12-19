from typing import Type

from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, create_engine, ScalarResult, update

from datamanager.data_manager_interface import DataManagerInterface
from models import User, Movie


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.engine = create_engine(f"sqlite:///{db_file_name}", echo=True)

        self.Session = sessionmaker(bind=self.engine)

        self.session = self.Session()

    def get_all_users(self) -> ScalarResult[User]:

        results = self.session.execute(select(User)).scalars()

        return results

    def get_user_movies(self, user_id: int) -> ScalarResult[Movie]:

        results = self.session.execute(
            select(Movie).filter_by(user_id=user_id)).scalars()

        return results

    def get_user(self, user_id: int) -> Type[User] | None:
        return self.session.get(User, user_id)

    def get_movie(self, movie_id: int) -> Type[Movie] | None:
        return self.session.get(Movie, movie_id)

    def add_user(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.commit()
            print(f"Added: {user}")
        except Exception as e:
            self.session.rollback()
            print(f"Error adding User: {e}")
        finally:
            self.session.close()

    def add_movies(self, movie: Movie) -> None:
        try:
            self.session.add(movie)
            self.session.commit()
            print(f"Added: {movie}")
        except Exception as e:
            self.session.rollback()
            print(f"Error adding Movie: {e}")
        finally:
            self.session.close()

    def update_movies(self, movie: Movie):
        try:
            self.session.execute(update(Movie)
            .where(Movie.id == movie.id)
            .values(
                user_id=movie.user_id,
                name=movie.name,
                director=movie.director,
                year=movie.year,
                rating=movie.rating
            ))
            self.session.commit()
            print(f"Updated: {movie}")
        except Exception as e:
            self.session.rollback()
            print(f"Error updating Movie: {e}")
        finally:
            self.session.close()

    def delete_movies(self, movie_id):
        try:
            movie = self.get_movie(movie_id)
            self.session.delete(movie)
            self.session.commit()
            print(f"Deleted: {movie}")
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting Movie: {e}")
        finally:
            self.session.close()

    def close(self):
        self.session.close()
