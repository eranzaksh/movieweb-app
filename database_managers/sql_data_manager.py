from .data_manager_interface import DataManagerInterface
from .sql_database import User, Movie, users_and_movies, db


API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_file_name}"
        db.init_app(app)

    def get_all_users(self):
        users = db.session.query(User)
        return users


    def get_user_movies(self, user_id):
        pass
