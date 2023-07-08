import secrets

import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from database_managers.json_data_manager_interface import JSONDataManager, UserIdAlreadyExists, WrongPassword
from database_managers.add_movies_methods import MovieAlreadyExists, NotFoundException

secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key
data_manager = JSONDataManager('./storage_files/json_database.json')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', e=e), 404


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    user_movie = data_manager.fetch_movie_by_id(user_id, movie_id)
    if request.method == 'POST':
        director = request.form.get("director")
        rating = request.form.get("rating")
        release_date = request.form.get("year")
        data_manager.update_movie(user_id, movie_id, director, release_date, rating)
        return redirect(url_for("user_movies", user_id=user_id))
    return render_template("update_movie.html", user_id=user_id, movie=user_movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for("user_movies", user_id=user_id))


@app.route('/users/<int:user_id>/add_movie', methods=["POST"])
def add_movie(user_id):
    movie_name = request.form.get("name")
    try:
        data_manager.add_movie(user_id, movie_name, "Director", "imdbRating", "Year", "Poster", "imdbID")
        return redirect(url_for("user_movies", user_id=user_id))
    except MovieAlreadyExists:
        flash("Movie already exist on your list!")
        return redirect(url_for("user_movies", user_id=user_id))
    except NotFoundException:
        flash("Movie not found on the database!")
        return redirect(url_for("user_movies", user_id=user_id))


@app.route('/authenticate_user/<int:user_id>', methods=["GET", "POST"])
def authenticate_user(user_id):
    try:
        if request.method == 'POST':
            users = data_manager.get_all_users()
            user = data_manager.fetch_user_by_id(user_id, users)
            login_password = request.form.get('password')
            hashed_pass = user['password']
            data_manager.authenticate_user(login_password, hashed_pass)
            return redirect(url_for("user_movies", user_id=user_id))
        return render_template("authenticate_user.html", user_id=user_id)
    except WrongPassword:
        flash('Incorrect password!')
        return render_template('authenticate_user.html', user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            users = data_manager.get_all_users()
            user_id = max(users, key=lambda x: x['id'])
            user_id = user_id['id'] + 1
            data_manager.add_user(name, user_id, password, confirm_password)
            return redirect(url_for("list_users"))
        return render_template('add_user.html')
    except UserIdAlreadyExists:
        flash("User Already Exists!")
        return render_template('add_user.html')
    except TypeError:
        flash("Passwords don't match!")
        return render_template('add_user.html')
    except WrongPassword:
        flash("Password needs to be at least 8 characters")
        return render_template('add_user.html')


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    user = data_manager.get_user_movies(user_id)
    user_name = data_manager.fetch_user_by_id(user_id, data_manager.get_all_users())
    return render_template('/user_movies.html', user=user, user_id=user_id, user_name=user_name)


@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
        return render_template('/users.html', users=users)
    except NotFoundException:
        return "File does not exists!"


@app.route('/')
def home():
    return render_template("/index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
