import json
import os
import requests
import bcrypt
from .data_manager_interface import DataManagerInterface
from .add_movies_methods import AddMovieMethods, NotFoundException

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class UserAlreadyExists(Exception):
    pass


class WrongPassword(Exception):
    pass


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def fetch_movie_by_id(self, user_id, movie_id):
        """
        Return a movie of a user based on the user id and movie id
        """
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:
                return movie

    @staticmethod
    def fetch_user_by_id(user_id, users):
        """
        Return user object from all users based on the user id
        """
        users = users
        for user in users:
            if user['id'] == str(user_id):
                return user

    def save_json_file(self, data):
        """
        Saving new data to the json file
        """
        json_data = json.dumps(data)
        with open(self.filename, 'w') as handle:
            handle.write(json_data)
        return json_data

    def list_users(self):
        """
        Return data of users from the json file, raise exception if the file doesn't exist
        """
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as handle:
                if os.path.getsize(self.filename) == 0:
                    return
                json_database = json.load(handle)
            return json_database
        else:
            raise NotFoundException(f"File {self.filename} doesn't exist")

    def update_movie(self, user_id, movie_id, director, date, rating):
        """
        Updating a movie, can update its director, date, and rating.
        """
        all_users = self.get_all_users()
        current_user = self.fetch_user_by_id(user_id, all_users)
        updated_movie = {"director": director, "year": date, "rating": rating}
        for movie in current_user['movies']:
            if movie['id'] == movie_id:
                movie.update(updated_movie)
        self.save_json_file(all_users)

    def delete_movie(self, user_id, movie_id):
        """
        Deleting movie form the json file based on user id and movie id
        """
        all_users = self.get_all_users()
        current_user_movie = self.fetch_movie_by_id(user_id, movie_id)
        user = self.fetch_user_by_id(user_id, all_users)
        user['movies'].remove(current_user_movie)
        self.save_json_file(all_users)

    def add_movie(self, user_id, name, director, rating, year, poster, imdb_page):
        """
        Adding movie to the database based on parameters received from the app.py and sending them to the OMDB api
        Then save the information on the json file
        """
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

    @staticmethod
    def authenticate_user(user_pass, hashed_pass):
        """
        Check if the password the user entered on the website
        match the password which is stored in the json file
        """
        if bcrypt.checkpw(user_pass.encode("utf-8"), hashed_pass.encode("utf-8")):
            return
        else:
            raise WrongPassword

    @staticmethod
    def create_user_password(password, confirm_password):
        """
        Checking password is at least 8 characters and same as confirm_password
         Then hashing the password and adding salt for better security
         return the hashed password
        """
        salt = bcrypt.gensalt()
        if password != confirm_password:
            raise TypeError("passwords don't match!")
        if len(password) < 8:
            raise WrongPassword("Password needs to be at least 8 characters")
        password = password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password, salt).decode("utf-8")
        return hashed_password

    def add_user(self, name, user_id, password, confirm_password):
        """
        Adding user with name, user_id and password (confirm_password should be the same as password)
        getting them all from the app.py
        """
        users = self.get_all_users()
        users_ids = [user['id'] for user in users]
        user_names = [user['name'] for user in users]
        hashed_pass = self.create_user_password(password, confirm_password)
        new_user = {"id": str(user_id), "name": name, "password": hashed_pass, "movies": []}
        if new_user['id'] in users_ids or new_user['name'] in user_names:
            raise UserAlreadyExists
        users.append(new_user)
        self.save_json_file(users)

    def get_all_users(self):
        """
        Getter for all users in the json file
        """
        try:
            all_users = self.list_users()
            return all_users
        except NotFoundException as e:
            return e

    def get_user_movies(self, user_id):
        """
        List all the user movies based on user id
        """
        all_users = self.get_all_users()
        user = self.fetch_user_by_id(user_id, all_users)
        if user:
            return user['movies']
        else:
            raise Exception("User not existing!")
