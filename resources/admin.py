from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import login_user

from playhouse.shortcuts import model_to_dict

import models

user = Blueprint('users', 'user', url_prefix='/user')


@user.route('/register', methods=["POST"])
def register():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        # Try to find an existing user in the database
        # If there's no user with this email, this should raise an exception
        models.Admin.get(models.Admin.email == payload['email'])
        # If there was a user with this email, return an error
        return jsonify(data={}, status={'code': 401, 'message': 'A user with this email already exists'})
    except models.DoesNotExist:
        # If the user doesn't exist, create the new user
        payload['password'] = generate_password_hash(payload['password'])
        user = models.Admin.create(**payload)

        # start a user session
        login_user(user)

        # turn user model into a dictionary so we jsonify it
        user_data = model_to_dict(user)

        # remove the password, since the client shouldn't need it
        del user_data['password']

        return jsonify(data=user_data, status={'code': 200, 'message': 'Success'})


@user.route('/login', methods=["POST"])
def login():
    payload = request.get_json()
    payload['email'] = payload['email'].lower()
    try:
        user = models.Admin.get(models.Admin.email == payload['email'])
        # we found a user, so check the password
        if check_password_hash(user.password, payload['password']):
            # password is correct, so log the user in
            login_user(user)
            # send back the user data from the database, just in case the client needs it
            user_data = model_to_dict(user)
            del user_data['password']
            return jsonify(data=user_data, status={'code': 200, 'message': 'Success'})
        else:
            return jsonify(data={}, status={'code': 401, 'message': 'Incorrect password'})
    except models.DoesNotExist:
        return jsonify(data={}, status={'code': 401, 'message': 'User does not exist'})