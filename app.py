import os
import secrets
from flask import Flask, render_template, request, redirect, url_for, flash
from database_managers.json_data_manager_interface import JSONDataManager, WrongPassword, UserAlreadyExists, \
    NotFoundException
from database_managers.add_movies_methods_json import MovieAlreadyExists
from database_managers.user_data_manager import User
from database_managers.sql_data_manager import SQLiteDataManager
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = secret_key
login_manager = LoginManager()
login_manager.init_app(app)

current_dir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(current_dir, 'storage_files', 'favorites_movies.sqlite')

data_manager = SQLiteDataManager(db_path, app)


@app.route('/logout')
@login_required
def logout():
    # Log out the user and clear the session
    logout_user()
    flash('Logged out successfully!')
    return redirect(url_for('home'))


@login_manager.user_loader
def loader_user(user_id):
    """
    Creating user object from a user in the json file to use for the flask_login
    """
    users = data_manager.get_all_users()
    user_data = data_manager.fetch_user_by_id(user_id)
    if user_data:
        user = User(user_data)
        return user


@app.errorhandler(404)
def page_not_found(e):
    """
    Page for displaying 404 errors
    """
    return render_template('404.html', e=e), 404


@app.errorhandler(401)
def forbidden_access(e):
    """
    Page for displaying 401 errors
    """
    return render_template('401.html', e=e), 401


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["GET", "POST"])
@login_required
def update_movie(user_id, movie_id):
    """
     A page to update some movie fields when the user presses on the "update" button.
    """
    user_movie = data_manager.fetch_user_movie_by_id(user_id, movie_id)
    if request.method == 'POST':
        watched = request.form.get("watched")
        user_rating = request.form.get("user_rating")
        data_manager.update_movie(user_id, movie_id, watched, user_rating)
        return redirect(url_for("user_movies", user_id=user_id))
    return render_template("update_movie.html", user_id=user_id, movie=user_movie)


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=["POST"])
@login_required
def delete_movie(user_id, movie_id):
    """
    Deleting a movie from the database when the user clicks on "Delete" button on the website
    """
    data_manager.delete_movie(user_id, movie_id)
    return redirect(url_for("user_movies", user_id=user_id))


@app.route('/users/<int:user_id>/add_movie', methods=["POST"])
@login_required
def add_movie(user_id):
    """
    Adding movie to the user logged on based on the movie_name the user typing on the website.
    Handling exceptions.
    """
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
    """
    Checking the hashed password with password the user entered on the website
    Creating user object for session authentication with flask_login.
    If no exception happen - login the user to the session using 'login_user'
    """
    user = data_manager.fetch_user_by_id(user_id)
    try:
        if request.method == 'POST':
            login_password = request.form.get('password')
            hashed_pass = data_manager.get_user_hashed_password(user_id)
            data_manager.authenticate_user(login_password, hashed_pass)
            user_obj = User(user)
            login_user(user_obj)
            return redirect(url_for("user_movies", user_id=user_id))
        return render_template("authenticate_user.html", user_id=user_id, user_name=user)
    except WrongPassword:
        flash('Incorrect password!')
        return render_template('authenticate_user.html', user_id=user_id, user_name=user)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
    A web page for adding a user, getting name,password, confirmed_password from the user
     and give the user a unique id.
     Handling exception in case of password or user problems
    """
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm-password')
            data_manager.add_user(name, password, confirm_password)
            return redirect(url_for("list_users"))
        return render_template('add_user.html')
    except UserAlreadyExists:
        flash("User Already Exists!")
        return render_template('add_user.html')
    except TypeError:
        flash("Passwords don't match!")
        return render_template('add_user.html')
    except WrongPassword:
        flash("Password needs to be at least 8 characters")
        return render_template('add_user.html')


@app.route('/users/<int:user_id>', methods=['GET'])
@login_required
def user_movies(user_id):
    """
    Display a user's movies using the json_data_manager
    """
    if current_user.get_id() != str(user_id):
        flash("Unauthorized, login required!")
        return redirect(url_for("list_users"))
    user = data_manager.get_user_movies(user_id)
    user_name = data_manager.fetch_user_by_id(user_id)
    return render_template('/user_movies.html', user=user, user_id=user_id, user_name=user_name)


@app.route('/users')
def list_users():
    """
    Listing all users from the json_data_manager and displaying in a web page
    """
    try:
        users = data_manager.get_all_users()
        return render_template('/users.html', users=users)
    except NotFoundException:
        return "File does not exists!"


@app.route('/')
def home():
    """
    Main web page
    """
    return render_template("/index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5005)
