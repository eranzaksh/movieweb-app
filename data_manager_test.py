import pytest
from database_managers.json_data_manager_interface import JSONDataManager


def test_json_add():
    data = JSONDataManager('./storage_files/testing.json')
    assert data.add_movie(3, "dark knight", "Director", "imdbRating", "Year", "Poster", "imdbRating")

