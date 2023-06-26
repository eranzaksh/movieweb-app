import csv
from data_manager_interface import DataManagerInterface


class CSVDataManagerInterface(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        pass

    def get_user_movies(self, user_id):
        pass
