import json

from dotenv import load_dotenv

import requests
import os

from requests import RequestException

from models import Movie

MOVIE_API_URL = "https://www.omdbapi.com/"


def get_key() -> str:
    load_dotenv()

    return os.getenv('key')


def get_parameters(movie_title: str) -> str:
    return f"?t={movie_title}&apikey="


def get_movie_data_from_api(movie_title: str) -> Movie:
    try:
        response = requests.get(
            MOVIE_API_URL + get_parameters(movie_title) + get_key(),
            verify=True,  # verify SSL Certificates
            timeout=5)  # 5 seconds timeout

        response.raise_for_status()  # Raises HTTPError for bad responses

        if response.status_code == 200:
            if response.json()["Response"] == 'True':
                movie = Movie()
                movie.year = response.json()["Year"]
                movie.rating = response.json()["imdbRating"]
                movie.director = response.json()["Director"]
                return movie
            else:
                raise Exception("Response is False")
        else:
            raise Exception("Status code is not 200")

    except requests.exceptions.RequestException:
        raise RequestException
    except ValueError:
        raise ValueError
    except Exception:
        raise Exception(
            "Please check if the .env file exists or if the key exists.")
