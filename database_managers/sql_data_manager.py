from ..app import app, db
from flask_sqlalchemy import SQLAlchemy
from .data_manager_interface import DataManagerInterface
from sql_database import User, Movie, users_and_movies


API_KEY = "711e7593"
URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t="


class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        self.db = SQLAlchemy(db_file_name)

    def get_all_users(self):
        users = db.session.query(User)
        return users

    @abstractmethod
    def get_user_movies(self, user_id):
        pass
