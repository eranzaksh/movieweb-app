from flask import Flask, render_template
from database_managers.json_data_manager_interface import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('./storage_files/json_database.json')


@app.route('/users/int:<user_id>/delete_movie/int:<movie_id>')


@app.route('/users/int:<user_id>/edit_movie/int:<movie_id>')


@app.route('/users/int<user_id>/update_movie/int:<movie_id>')


@app.route('/users/int:<user_id>/add_movie')


@app.route('/add_user')


@app.route('/users/int:<user_id>')
def user_movies(user_id):
    pass


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('/users.html', users=users)


@app.route('/')
def home():
    return "Welcome to Movieweb app!"


if __name__ == "__main__":
    app.run(debug=True)
