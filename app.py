import requests
from flask import Flask, render_template, request, redirect, url_for, flash
from database_managers.json_data_manager_interface import JSONDataManager, MovieAlreadyExists, NotFoundException, \
    UserIdAlreadyExists

app = Flask(__name__)
data_manager = JSONDataManager('./storage_files/json_database.json')


# @app.route('/users/int:<user_id>/edit_movie/int:<movie_id>')
#
#
# @app.route('/users/int<user_id>/update_movie/int:<movie_id>')
#
#
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for("user_movies", user_id=user_id))


@app.route('/users/<int:user_id>/add_movie', methods=["POST"])
def add_movie(user_id):
    movie_name = request.form.get("name")
    try:
        data_manager.add_movie(user_id, movie_name, "Director", "imdbRating", "Year", "Poster", "imdbRating")
        return redirect(url_for("user_movies", user_id=user_id))
    except MovieAlreadyExists:
        return redirect(url_for("user_movies", user_id=user_id))
    except NotFoundException:
        return redirect(url_for("user_movies", user_id=user_id))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            users = data_manager.get_all_users()
            user_id = max(users, key=lambda x: x['id'])
            user_id = user_id['id'] + 1
            data_manager.add_user(name, user_id)
            return redirect(url_for("list_users"))
        return render_template('add_user.html')
    except UserIdAlreadyExists:
        return "User Already Exists"


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    user = data_manager.get_user_movies(user_id)
    return render_template('/user_movies.html', user=user, user_id=user_id)


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
    app.run(debug=True)
