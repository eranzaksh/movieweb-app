import json
import os

import requests

from .data_manager_interface import DataManagerInterface

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class MovieAlreadyExists(Exception):
    pass


class NotFoundException(Exception):
    pass


class UserIdAlreadyExists(Exception):
    pass


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def fetch_movie_by_id(self, user_id, movie_id):
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:
                return movie

    @staticmethod
    def fetch_user_by_id(user_id, users):
        users = users
        for user in users:
            if user['id'] == user_id:
                return user

    def save_json_file(self, data):
        json_data = json.dumps(data)
        with open(self.filename, 'w') as handle:
            handle.write(json_data)
        return json_data

    def list_movies(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as handle:
                if os.path.getsize(self.filename) == 0:
                    return
                json_database = json.load(handle)
            return json_database
        else:
            raise NotFoundException(f"File {self.filename} doesn't exist")

    def delete_movie(self, user_id, movie_id):
        all_users = self.get_all_users()
        current_user_movie = self.fetch_movie_by_id(user_id, movie_id)
        user = self.fetch_user_by_id(user_id, all_users)
        user['movies'].remove(current_user_movie)
        self.save_json_file(all_users)

    def add_movie(self, user_id, name, director, rating, year, poster, imdb_page):
        movies_list = self.get_user_movies(user_id)
        users = self.get_all_users()
        if movies_list is None:
            movies_list = {}
        try:
            res = requests.get(URL + name)
            movie_data = res.json()
            for movie in movies_list:
                if name.lower() in movie["name"].lower():
                    raise MovieAlreadyExists
            if 'Error' in movie_data:
                raise NotFoundException("Movie not found!")
            movie_id = len(movies_list)
            for movie in movies_list:
                if movie_id == movie['id']:
                    movie_id += 1
            new_movie = {"id": movie_id, "name": movie_data["Title"], 'rating': float(movie_data[rating]),
                         'year': movie_data[year],
                         'poster': movie_data[poster], 'page': movie_data[imdb_page], 'director': movie_data[director]}
            for user in users:
                if user['id'] == user_id:
                    user['movies'].append(new_movie)
            self.save_json_file(users)
            return
        except requests.exceptions.RequestException:
            print("There is no internet connection!")

    def add_user(self, name, user_id):
        users = self.get_all_users()
        users_ids = [user['id'] for user in users]
        new_user = {"id": user_id, "name": name, "movies": []}
        if users is None:
            users = []
        if new_user['id'] in users_ids:
            raise UserIdAlreadyExists
        users.append(new_user)
        self.save_json_file(users)

    def get_all_users(self):
        try:
            all_users = self.list_movies()
            return all_users
        except NotFoundException as e:
            return e

    def get_user_movies(self, user_id):
        # return a list of all movies for given user
        all_users = self.list_movies()
        user_movies = [user for user in all_users if user['id'] == user_id]
        if user_movies:
            return user_movies[0].get('movies')
        else:
            raise Exception("User not existing!")
