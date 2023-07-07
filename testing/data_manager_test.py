import pytest
from ..database_managers.json_data_manager_interface import JSONDataManager, UserIdAlreadyExists
from ..database_managers.add_movies_methods import NotFoundException
import random

movie_names = [
    "The Shawshank Redemption",
    "The Godfather",
    "Pulp Fiction",
    "Fight Club",
    "The Lord of the Rings: The Fellowship of the Ring",
    "Goodfellas",
    "The Matrix",
    "The Avengers",
    "Jurassic Park",
    "Star Wars: Episode IV - A New Hope"
]


def test_json_users_exception():
    data_manager = JSONDataManager('./storage_files/invalid_file.json')
    result = data_manager.get_all_users()
    assert isinstance(result, NotFoundException)


def test_json_users_no_exception():
    data_manager = JSONDataManager('testing/testing.json')
    users = data_manager.get_all_users()
    assert isinstance(users, list)


def test_json_add():
    data = JSONDataManager('testing/testing.json')
    movies = data.get_user_movies(1)
    before_movies = len(movies)
    data.add_movie(1, movie_names[random.randint(0, 9)], "Director", "imdbRating", "Year", "Poster", "imdbRating")
    after_movies = len(data.get_user_movies(1))
    assert before_movies != after_movies


def test_json_delete():
    data = JSONDataManager('testing/testing.json')
    movies = data.get_user_movies(1)
    movies_id = [movie['id'] for movie in movies]
    before_movies = len(movies)
    data.delete_movie(1, random.choice(movies_id))
    after_movies = len(data.get_user_movies(1))
    assert before_movies != after_movies


def test_add_user():
    data_manager = JSONDataManager("testing/testing_users.json")
    data_manager.add_user("david", 8)
    users = data_manager.get_all_users()
    assert len(users) == 2
    assert users[1]['name'] == 'david'
    assert users[1]['id'] == 8


def test_add_user_exception():
    data_manager = JSONDataManager("testing/testing_users.json")
    user_id = data_manager.get_all_users()[0]['id']
    user_name = data_manager.get_all_users()[0]['name']
    with pytest.raises(UserIdAlreadyExists):
        data_manager.add_user(user_name, user_id)

