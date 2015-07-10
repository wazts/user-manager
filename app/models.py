"""
    views.py
--------------------------------------------------------------------------------
    The RESTful endpoints for the user manager
--------------------------------------------------------------------------------
    @author Kyle Wagner
    @date 2015
--------------------------------------------------------------------------------
"""

import jwt
import uuid
from app import db, bcrypt
from flask.ext.sqlalchemy import SQLAlchemy

class User(db.Model):
    """ The user model
        The user for the system. This includes their status, state, password
        hash, and username.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    jwt_secret = db.Column(db.String(128))
    
    def hash_password(self, password):
        """ Hash the password for our user
            This hashes and places the password into the model so it's safer
        """
        self.password_hash = bcrypt.generate_password_hash(password)
        return self.password_hash

    def verify_password(self, password):
        """ Checks the password against the hash
            Checks the password against the hash and returns true or false if
            password is correct.
        """
        return bcrypt.check_password_hash(self.password_hash, password)
        
    def generate_login_token (self, newSecret=True):
        
        secret = ""
        if newSecret or self.jwt_secret == "":
            secret = str(uuid.uuid4())
        else:
            secret = self.jwt_secret
            
        self.jwt_secret = secret
        db.session.add (self)
        db.session.commit()
        
        return jwt.encode({'user': self.id}, secret, algorithm='HS256')
        
    def verify_login_token (self, token):
        try:
            jwt.decode(token, self.jwt_secret, algorithms=['HS256'])
        except jwt.InvalidTokenError:
            return None
        return self
        
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.hash_password(password)

    def __repr__(self):
        return '<User %r>' % self.username