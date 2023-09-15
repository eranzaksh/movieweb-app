import bcrypt
from .data_manager_interface import DataManagerInterface
import requests
from .sql_database import User, Movie, users_and_movies, db_orm, Reviews
from sqlalchemy.orm.exc import NoResultFound


API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class WrongPassword(Exception):
    pass


class UserAlreadyExists(Exception):
    pass


class MovieAlreadyExists(Exception):
    pass


class NotFoundException(Exception):
    pass


class SQLiteDataManager(DataManagerInterface):

    def __init__(self, db):
        self.db_orm = db

    def get_all_users(self):
        """
        :return: all users from the database
        """
        return db_orm.session.query(User)

    @staticmethod
    def fetch_review_by_id(review_id):
        """
        return a review based on given review id
        """
        return db_orm.session.query(Reviews).filter(Reviews.id == review_id).one()

    @staticmethod
    def get_reviewed_movies():
        """
        returns all movies and their reviews
        """
        return db_orm.session.query(Movie, Reviews).join(Reviews).all()

    @staticmethod
    def get_all_movies():
        """
        :return: all movies from the database
        """
        return db_orm.session.query(Movie)

    def get_user_movies(self, user_id):
        """
        return all movies for a user
        """
        movies = db_orm.session.query(Movie, users_and_movies.c.user_rating, users_and_movies.c.watched) \
            .join(users_and_movies, users_and_movies.c.movie_id == Movie.id) \
            .filter(users_and_movies.c.user_id == user_id).all()
        return movies

    @staticmethod
    def fetch_user_by_id(user_id):
        """
        return a user object from the database based on the id
        """
        user = db_orm.session.query(User).filter(User.id == user_id).first()
        return user

    @staticmethod
    def fetch_user_movie_by_id(user_id, movie_id):
        """
        return a movie, based on movie_id, for a user based on user_id
        """
        movie_data = db_orm.session.query(Movie, users_and_movies.c.user_rating, users_and_movies.c.watched) \
            .join(User.movie) \
            .join(users_and_movies) \
            .filter(User.id == user_id).filter(Movie.id == movie_id).first()
        return movie_data

    def update_review(self, updated_review, review_id):
        """
        updating a review based on the review_id
        """
        current_review = self.fetch_review_by_id(review_id)
        current_review.review = updated_review
        db_orm.session.commit()
        return

    @staticmethod
    def delete_review(review_id):
        """
        delete a review based on review_id
        """
        a_movie_review = db_orm.session.query(Reviews).filter(Reviews.id == review_id).one()
        db_orm.session.delete(a_movie_review)
        db_orm.session.commit()
        return

    @staticmethod
    def add_review(movie_id, review, user_id):
        """
        add a new review to a movie from a user
        """
        new_review = Reviews(
            review=review,
            movie_id=movie_id,
            user_id=user_id
        )
        db_orm.session.add(new_review)
        db_orm.session.commit()
        return

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

    @staticmethod
    def update_movie(user_id, movie_id, watched, user_rating):
        """
        Updating a movie, can update the user rating or if watched.
        """
        db_orm.session.query(users_and_movies) \
            .filter(users_and_movies.c.movie_id == movie_id) \
            .filter(users_and_movies.c.user_id == user_id) \
            .update({users_and_movies.c.user_rating: user_rating, users_and_movies.c.watched: watched})
        db_orm.session.commit()
        return

    def delete_movie(self, user_id, movie_id):
        """
        remove the connection of a movie to a user, if that movie no longer have any user connections
        it gets deleted from the database
        """
        movie = self.fetch_user_movie_by_id(user_id, movie_id)
        user = self.fetch_user_by_id(user_id)
        user.movie.remove(movie[0])
        db_orm.session.commit()
        try:
            db_orm.session.query(users_and_movies.c.movie_id) \
                .filter(users_and_movies.c.movie_id == movie_id).one()
        except NoResultFound:
            try:
                movie = db_orm.session.query(Movie).filter(Movie.id == movie_id).one()
                db_orm.session.delete(movie)
                db_orm.session.commit()
                return
            except NoResultFound:
                return
