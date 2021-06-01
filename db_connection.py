from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os


class DbConnection:

    def __init__(self, app: Flask) -> None:
        self.app = app

        load_dotenv()
        env_path = os.getcwd() + '/.env '
        load_dotenv(env_path)

        # Database Config
        self.app.config['MONGO_URI'] = os.getenv('DB_CONNECTION_URI')
        self.mongo = PyMongo(app)
        self.db = self.mongo.db.users
        # End Database Config

    def get_collection(self):
        return self.db
