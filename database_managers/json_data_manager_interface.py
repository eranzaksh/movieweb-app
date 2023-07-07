import json
import os
import requests
from flask_bcrypt import Bcrypt
from .data_manager_interface import DataManagerInterface
from .add_movies_methods import AddMovieMethods, NotFoundException

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


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

    def update_movie(self, user_id, movie_id, director, date, rating):
        all_users = self.get_all_users()
        current_user = self.fetch_user_by_id(user_id, all_users)
        updated_movie = {"director": director, "year": date, "rating": rating}
        for movie in current_user['movies']:
            if movie['id'] == movie_id:
                movie.update(updated_movie)
        self.save_json_file(all_users)

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
            new_movie = AddMovieMethods.generating_new_movie(name, movies_list, movie_data,
                                                             rating, year, poster, imdb_page, director)
            AddMovieMethods.add_movie_to_user(users, user_id, new_movie)
            self.save_json_file(users)
            return
        except requests.exceptions.RequestException:
            print("There is no internet connection!")

    def create_user_password(self, password, confirm_password):
        bcrypt = Bcrypt()
        if password != confirm_password:
            raise Exception("passwords don't match!")
        password = bcrypt.generate_password_hash(password).decode('utf-8')
        pass

    def add_user(self, name, user_id, password, confirm_password):
        users = self.get_all_users()
        users_ids = [user['id'] for user in users]
        user_names = [user['name'] for user in users]
        hashed_pass = self.create_user_password(password, confirm_password)
        new_user = {"id": user_id, "name": name, "password": hashed_pass, "movies": []}
        if users is None:
            users = []
        if new_user['id'] in users_ids or new_user['name'] in user_names:
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
