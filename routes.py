from flask import Flask, json, request, jsonify
from crud import Crud
from user import User


class Routes:

    def __init__(self, app: Flask) -> None:
        self.app = app

        crud = Crud(app)

        @app.route('/create_user', methods=['POST'])
        def create_user():
            user = User(
                request.json['name'], request.json['email'], request.json['password'], '')
            id = str(crud.create_user(user))
            if id != '':
                return jsonify({'Message': 'User Saved on DataBase'}, {'_id': id})
            else:
                return jsonify({'Message': 'User Cannot Be Saved on DataBase'})

        @app.route('/get_users', methods=['GET'])
        def get_users():
            users = crud.get_all_users()
            return jsonify(users)

        @app.route('/get_user/<id>', methods=['GET'])
        def get_user(id):
            user = crud.get_user(id)
            return jsonify(user)

        @app.route('/delete_user/<id>', methods=['DELETE'])
        def delete_user(id):
            if crud.delete_user(id):
                return jsonify({'Message': 'Deleted'})
            else:
                return jsonify({'Message': 'Not Deleted'})

        @app.route('/update_user/<id>', methods=['PUT'])
        def update_user(id):
            user = User(
                request.json['name'], request.json['email'], request.json['password'])

            if crud.update_user(id, user):
                return jsonify({'Message': 'User Updated'})
            else:
                return jsonify({'Message': 'Cannot Update User'})
            return 'received'

        @app.route('/upload_image/<id>', methods=['PUT'])
        def upload_image(id):
            if request.method == 'PUT':
                # file = nombre que se le dara al form data
                file = request.files['file']
                status = crud.upload_image(file, id)
                return jsonify(status)

        @app.route('/get_image/<id>', methods=['GET'])
        def get_image(id):
            return crud.get_image(id)
