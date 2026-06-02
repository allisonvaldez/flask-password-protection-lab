# Import necessary components and utilities for the app
from sqlalchemy.ext.hybrid import hybrid_property
from marshmallow import Schema, fields
from config import db, bcrypt

# Createa a class for the user model to register
class User(db.Model):
    __tablename__ = 'users'

    # Declare a column to store unique id for users
    id = db.Column(db.Integer, primary_key=True)

    # Declare a column to store usernames
    username = db.Column(db.String)

    # Declare a column to store the hashed passwords
    _password_hash = db.Column(db.String)

    # Using a hybrid decorator create a method for password protection
    @hybrid_property
    def password_hash(self):
        # Error handling if issues
        raise AttributeError('Password hash is not readable')

    # Use a setter decorator to create a function to provide password hash ability
    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a function for authentication
    def authenticate(self, password):
        return bcrypt.check_password_hash(self._password_hash, password)

    def __repr__(self):
        return f'User {self.username}, ID: {self.id}'


# Create a class for the Marshmallow schema for JSON data
class UserSchema(Schema):
    id = fields.Int()
    username = fields.String()