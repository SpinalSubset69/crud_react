from flask import Flask, send_from_directory
from flask_pymongo import ObjectId
import pymongo
from user import User
from db_connection import DbConnection
import os


class Crud:

    def __init__(self, app: Flask):
        self.app = app
        conn = DbConnection(app)
        self.db = conn.get_collection()

    # Operations

    def create_user(self, user: User):
        try:
            id = self.db.insert({
                "name": user.name,
                "email": user.email,
                "password": user.password
            })
            return id
        except Exception as e:
            print(str(e))

    def get_user(self, id: str):
        try:
            user = self.db.find_one({'_id': ObjectId(id)})
            print(user)
            if user.get('image') != None:
                return {
                    '_id': str(ObjectId(user['_id'])),
                    'name': user['name'],
                    'email': user['email'],
                    'password': user['password'],
                    'image': user['image']
                }
            else:
                return {
                    '_id': str(ObjectId(user['_id'])),
                    'name': user['name'],
                    'email': user['email'],
                    'password': user['password']
                }
        except Exception as e:
            print(str(e))

    def get_all_users(self):
        try:
            users = []
            for user in self.db.find({}).sort('_id', pymongo.DESCENDING):
                if user.get('image') != None:
                    users.append({
                        '_id': str(ObjectId(user['_id'])),
                        'name': user['name'],
                        'email': user['email'],
                        'password': user['password'],
                        'image': user['image']
                    })
                else:
                    users.append({
                        '_id': str(ObjectId(user['_id'])),
                        'name': user['name'],
                        'email': user['email'],
                        'password': user['password']
                    })
            return users
        except Exception as e:
            print(str(e))

    def update_user(self, id: str, user: User):
        try:
            self.db.find_one_and_update({'_id': ObjectId(id)}, {'$set': {
                'name': user.name,
                'email': user.email,
                'password': user.password
            }})
            return True
        except Exception as e:
            print(str(e))

    def delete_user(self, id: str):
        try:
            user = self.get_user(id)
            # Verificamos la existencia de la clave en user
            if user.get('image') != None:
                os.remove(os.getcwd() + '/images/' + user['image'])
            self.db.delete_one({'_id': ObjectId(id)})
            return True
        except Exception as e:
            print(str(e))

    def upload_image(self, file, id):
        try:
            condicion = os.path.isfile(
                os.getcwd() + '/images/' + file.filename)
            print(condicion)
            if condicion:
                return {'Message': 'Image already exists'}
            else:
                file.save(os.getcwd() + '/images/' + file.filename)
                self.db.find_one_and_update({'_id': ObjectId(id)}, {'$set': {
                    'image': file.filename
                }})
                return {'Message': 'Image Uploaded'}
        except Exception as e:
            print(str(e))

    def get_image(self, id):
        user = self.db.find_one({'_id': ObjectId(id)})
        if user.get('image') != None:
            return send_from_directory(os.getcwd() + '/images/', user['image'])
        else:
            return {'Message': 'User didnt upload an image yet'}

    # End Operations
