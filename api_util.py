from dotenv import load_dotenv

import requests
import os

from requests import RequestException

from models import Movie

MOVIE_API_URL = "https://www.omdbapi.com/"


def get_key() -> str:
    """
    Retrieves the API key from the environment variables.

    Returns:
        str: The API key for accessing the OMDB API.
    """
    load_dotenv()

    return os.getenv('key')


def get_parameters(movie_title: str) -> str:
    """
    Constructs the query parameters for the API request.

    Parameter:
        movie_title (str): The title of the movie.

    Returns:
        str: The query parameters as a string.
    """
    return f"?t={movie_title}&apikey="


def get_movie_data_from_api(movie_title: str) -> Movie:
    """
    Fetches movie data from the OMDB API and maps it to a Movie object.

    Parameter:
        movie_title (str): The title of the movie to search for.

    Returns:
        Movie: A Movie object containing the retrieved data.

    Raises:
        RequestException: If the request fails.
        ValueError: If the JSON response cannot be decoded or is invalid.
        Exception: If the API response indicates failure or unexpected issues occur.
    """
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

                rating_str = response.json()["imdbRating"]

                if rating_str == "N/A":
                    movie.rating = 0.0
                else:
                    movie.rating = response.json()["imdbRating"]
                movie.director = response.json()["Director"]
                movie.path = response.json()["Poster"]
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
