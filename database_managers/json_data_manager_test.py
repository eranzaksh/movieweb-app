import os
from random import randint
import secrets
import pytest
from .json_data_manager_interface import JSONDataManager, WrongPassword, UserAlreadyExists
from .add_movies_methods import NotFoundException, MovieAlreadyExists
import json


def test_json_users_exception():
    data_manager = JSONDataManager('./storage_files/invalid_file.json')
    result = data_manager.get_all_users()
    assert isinstance(result, NotFoundException)


def test_json_users_no_exception():
    data_manager = JSONDataManager('testing/testing.json')
    users = data_manager.get_all_users()
    assert isinstance(users, list)


def test_get_user_movies():
    data_manager = JSONDataManager('testing/testing.json')
    user = data_manager.get_user_movies("1")


def test_add_user_to_empty_json():
    json_data = []
    filepath = 'json_data.json'
    with open(filepath, 'w') as fileobj:
        json.dump(json_data, fileobj)
    data_manager = JSONDataManager(filepath)
    data_manager.add_user("qwe", "100", "123qweasd", "123qweasd")
    assert len(data_manager.get_all_users()) == 1
    os.remove(filepath)


def test_user_already_exists():
    data_manager = JSONDataManager('testing/testing.json')
    rand_name = secrets.token_hex(4)
    user_id = "1234567"
    data_manager.add_user(rand_name, user_id, "123qweasd", "123qweasd")
    with pytest.raises(UserAlreadyExists):
        data_manager.add_user(rand_name, user_id, "123qweasd", "123qweasd")


def test_add_movie():
    data = JSONDataManager('testing/testing.json')
    data.add_movie("1", "titanic", "Director", "imdbRating", "Year", "Poster", "imdbRating")
    movies = data.get_user_movies(1)
    movie_id = max(movies, key=lambda x: x['id'])['id']
    assert data.fetch_movie_by_id('1', movie_id)['name'] == "Titanic"
    data.delete_movie("1", movie_id)


def test_add_movie_list_none():
    rand_user_id = randint(101, 10000)
    rand_user_name = secrets.token_hex(6)
    data = JSONDataManager('testing/testing.json')
    data.add_user(rand_user_name, str(rand_user_id), "123qweasd", "123qweasd")
    data.add_movie(str(rand_user_id), "titanic", "Director", "imdbRating", "Year", "Poster", "imdbRating")
    assert len(data.get_user_movies(str(rand_user_id))) == 1


def test_movie_not_found():
    with pytest.raises(NotFoundException):
        data = JSONDataManager('testing/testing.json')
        data.add_movie("1", "trfjrtkdfgk", "Director", "imdbRating", "Year", "Poster", "imdbRating")


def test_movie_already_exists():
    with pytest.raises(MovieAlreadyExists):
        data = JSONDataManager('testing/testing.json')
        data.add_movie("1", "bambi", "Director", "imdbRating", "Year", "Poster", "imdbRating")


def test_passwords_dont_match():
    data = JSONDataManager('testing/testing.json')
    with pytest.raises(TypeError):
        data.create_user_password("12345678", "12345679")


def test_password_too_short():
    data = JSONDataManager('testing/testing.json')
    with pytest.raises(WrongPassword):
        data.create_user_password("123", "123")
