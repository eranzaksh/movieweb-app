import pytest
from database_managers.json_data_manager_interface import JSONDataManager


def test_json_add():
    data = JSONDataManager('./storage_files/testing.json')
    movies = data.get_user_movies(1)
    print(movies)

