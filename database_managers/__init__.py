from .sql_data_manager import SQLiteDataManager
from .sql_database import db_orm

data_manager = SQLiteDataManager(db_orm)
