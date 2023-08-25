import bcrypt
import requests
from sqlalchemy import and_
from .json_data_manager_interface import WrongPassword, UserAlreadyExists
from .add_movies_methods_json import MovieAlreadyExists, NotFoundException
from .data_manager_interface import DataManagerInterface
from .sql_database import User, Movie, users_and_movies, db_orm

API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file_name}"
        db_orm.init_app(app)

    def get_all_users(self):
        users = db_orm.session.query(User)
        return users

    def get_user_movies(self, user_id):
        movies = db_orm.session.query(Movie).join(User.movie).filter(User.id == user_id).all()
        return movies

    @staticmethod
    def fetch_user_by_id(user_id):
        user = db_orm.session.query(User).filter(User.id == user_id).first()
        return user

    def fetch_user_movie_by_id(self, user_id, movie_id):
        user = self.fetch_user_by_id(user_id)
        for movie in user.movie:
            if movie.id == movie_id:
                return movie


    @staticmethod
    def authenticate_user(user_pass, hashed_pass):
        """
        Check if the password the user entered on the website
        match the password which is stored in the json file
        """
        if bcrypt.checkpw(user_pass.encode("utf-8"), hashed_pass[0].encode("utf-8")):
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

    def add_user(self, name, password, confirm_password):
        """
        Adding user with name, user_id and password (confirm_password should be the same as password)
        getting them all from the app.py
        """
        hashed_pass = self.create_user_password(password, confirm_password)
        user = db_orm.session.query(User.name).filter(User.name == name).first()
        if user:
            raise UserAlreadyExists
        new_user = User(
            name=name,
            password=hashed_pass
        )
        db_orm.session.add(new_user)
        db_orm.session.commit()

    @staticmethod
    def get_user_hashed_password(user_id):
        password = db_orm.session.query(User.password).filter(User.id == user_id).first()
        return password

    @staticmethod
    def add_movie(user_id, name, director, rating, year, poster, imdb_page):
        """
        Adding movie to the database based on parameters received from the app.py and sending them to the OMDB api
        Then save the information on the sqlite file
        """
        try:
            res = requests.get(URL + name)
            movie_data = res.json()
            user = db_orm.session.query(User).filter(User.id == user_id).first()
            if 'Error' in movie_data:
                raise NotFoundException("Movie not found!")
            # movies = db_orm.session.query(Movie.name)
            existed_movie = db_orm.session.query(Movie).filter(Movie.name == movie_data["Title"]).first()
            # Check if the movie already exists in the Movie table. if it does, only add it to the user's list
            if existed_movie:
                # Check if movie already connected to the user
                if existed_movie in user.movie:
                    raise MovieAlreadyExists
                user.movie.append(existed_movie)
                db_orm.session.commit()
                return
            new_movie = Movie(
                name=movie_data["Title"],
                rating=movie_data[rating],
                year=movie_data[year],
                poster=movie_data[poster],
                page=movie_data[imdb_page],
                director=movie_data[director]
            )
            db_orm.session.add(new_movie)
            user.movie.append(new_movie)
            db_orm.session.commit()
            return
        except requests.exceptions.RequestException:
            print("There is no internet connection!")

    def update_movie(self, user_id, movie_id, director, year, rating):
        """
        Updating a movie, can update its director, date, and rating.
        """
        user = self.fetch_user_by_id(user_id)
        for movie in user.movie:
            if movie.id == movie_id:
                movie.director = director
                movie.year = year
                movie.rating = float(rating)
                db_orm.session.commit()
                return
                
    def delete_movie(self, user_id, movie_id):
        movie = self.fetch_user_movie_by_id(user_id, movie_id)
        user = self.fetch_user_by_id(user_id)
        user.movie.remove(movie)
        db_orm.session.commit()
        return
