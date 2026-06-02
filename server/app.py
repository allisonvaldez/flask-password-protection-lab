#!/usr/bin/env python3

# Import utilities and components for app
from flask import request, session
from flask_restful import Resource
from config import app, db, api
from models import User, UserSchema


# Create a function to reset session
class ClearSession(Resource):

    # Declare a function in charge of deletion
    def delete(self):
        session['page_views'] = None
        session['user_id'] = None
        return {}, 204


# Create a class to create user accounts with hashed password
class Signup(Resource):

    # Create a function to post
    def post(self):

        data = request.get_json()

        # Set users
        user = User(username=data.get('username'))

        # Set hashing for password
        user.password_hash = data.get('password')

        # Save users to the db
        db.session.add(user)
        db.session.commit()

        # Store user to session 
        session['user_id'] = user.id
        return UserSchema().dump(user), 201


# Create a class to verify if user is logged in
class CheckSession(Resource):

    # Create a function to verify 
    def get(self):

        user_id = session.get('user_id')

        # Perform error handling
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return UserSchema().dump(user), 200

        return {}, 204


# Create a class to authenticates users and stores id to session
class Login(Resource):

    # Create a function to do the heavy lifting of getting and setting username and password
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Seach db
        user = User.query.filter(User.username == username).first()

        # Control flow for match
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return UserSchema().dump(user), 200

        # Error handling
        return {'error': 'Invalid username or password'}, 401


# Create a class to logout users
class Logout(Resource):

    # Create a function to clear the session
    def delete(self):
        session['user_id'] = None
        return {}, 204


# Register each Resource
api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)