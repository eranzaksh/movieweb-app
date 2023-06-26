import requests
from flask import Flask, render_template, request, redirect, url_for
from database_managers.json_data_manager_interface import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('./storage_files/json_database.json')


# @app.route('/users/int:<user_id>/delete_movie/int:<movie_id>')
#
#
# @app.route('/users/int:<user_id>/edit_movie/int:<movie_id>')
#
#
# @app.route('/users/int<user_id>/update_movie/int:<movie_id>')
#
#
@app.route('/users/int:<user_id>/add_movie')
def add_movie():
    pass


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        users = data_manager.get_all_users()
        user_id = max(users, key=lambda x: x['id'])
        user_id = user_id['id'] + 1
        data_manager.add_user(name, user_id)
        return redirect(url_for("list_users"))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    user = data_manager.get_user_movies(user_id)
    return render_template('/user_movies.html', user=user, user_id=user_id)


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('/users.html', users=users)


@app.route('/')
def home():
    return "Welcome to Movieweb app!"


if __name__ == "__main__":
    app.run(debug=True)
