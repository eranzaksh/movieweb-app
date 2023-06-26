import json
import os

from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def list_movies(self):
        with open(self.filename, 'r') as handle:
            if os.path.getsize(self.filename) == 0:
                return
            json_database = json.load(handle)
        return json_database

    def get_all_users(self):
        all_users = self.list_movies()
        return all_users

    def get_user_movies(self, user_id):
        # return a list of all movies for given user
        all_users = self.list_movies()
        user_movies = [user for user in all_users if user['id'] == user_id]
        if user_movies:
            return user_movies[0].get('movies')
        else:
            raise Exception("User not existing!")


