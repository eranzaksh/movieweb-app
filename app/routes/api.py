from flask import Blueprint, jsonify
from database_managers import data_manager

api = Blueprint('api', __name__)


@api.route('/users', methods=['GET'])
def get_users():
    """
    Getting a list of all users in the database
    """
    users = [{"User": user.name, "id": user.id} for user in data_manager.get_all_users()]
    return jsonify(users)


@api.route('/users/<user_id>/movies', methods=["GET"])
def get_user_movies(user_id):
    """
    Getting all movies for a user
    """
    user_movies = [movie[0].name for movie in data_manager.get_user_movies(user_id)]
    return jsonify(user_movies)


@api.route('/movies', methods=["GET"])
def get_movies():
    """
    retrieve all movies in the database
    """
    movies = [{"name": movie.name, "id": movie.id} for movie in data_manager.get_all_movies()]
    return jsonify(movies)


@api.route('/movies/<movie_id>/reviews', methods=["GET"])
def get_movie_reviews(movie_id):
    """
    Gets all reviews for a movie
    """
    reviews = data_manager.get_reviewed_movies()
    reviews_for_movie = [review[1].review for review in reviews if review[0].id == int(movie_id)]
    return jsonify(reviews_for_movie)


@api.route('/movies/reviews', methods=["GET"])
def get_all_reviews():
    """
    Getting all reviews for every movie
    """
    all_reviews = data_manager.get_reviewed_movies()
    reviews = [{"movie": review[0].name, "reviews": review[1].review} for review in all_reviews]
    return jsonify(reviews)

