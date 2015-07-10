"""
    views.py
--------------------------------------------------------------------------------
    The RESTful endpoints for the user manager
--------------------------------------------------------------------------------
    @author Kyle Wagner
    @date 2015
--------------------------------------------------------------------------------
"""

from flask import Flask, request
from flask.ext.restful import Resource, Api, fields, marshal_with, reqparse, abort
from app.models import User
from app import api, db

import jwt

# --- Tokens

user_fields = {
    'uri': fields.Url('user_info'),
    'username': fields.String,
    'email' : fields.String
}

class LoginUser(Resource):
    """ Login the user
    
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)
    
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        
        u = User.query.filter_by(username=username).first()
        
        if u != None and u.verify_password(password):
            encoded = u.generate_login_token()
        else:
            abort (400, message="Login failure")
            
        return {"token" : encoded }

class UsersAllInfo(Resource):
    """ Get info for all users
    
    """
    
    @marshal_with(user_fields)
    def get(self):
        
        u = User.query.all()
        
        if u:
            return u
            
        abort(404, message="No users exist")

    """ Register the user
        Register a new user and return the user.
    """
    
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        user = User(username=args['username'], email=args['email'], password=args['password'])
        
        # Commit to the database
        
        db.session.add(user)
        
        try:
            db.session.commit()
        except:
            abort (404, message="User {} already exists".format(args['username']))
        
        return user
        
class UserInfo(Resource):
    """ Get the user
    
    """
    
    @marshal_with(user_fields)
    def get(self, id):
        
        u = User.query.filter_by(id=id).first()
        
        # Make sure we have the user
        if u:
            return u
        
        abort(404, message="User {} doesn't exist".format(id))

    """ Delete the user
        Delete the user if we have the rights
    """
    def delete(self, user_id):
        pass
        
class VerifiyUser(Resource):
    """ Verify the user
    
    """
    
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, required=True)
        
        args = parser.parse_args()
        
        try: 
            tokenPayload = jwt.decode(args['token'], verify=False)
        except jwt.InvalidTokenError:
            abort(403, message="Validation error")
        
        user = None
        if 'user' in tokenPayload:
            user = User.query.filter_by(id=tokenPayload['user']).first()
        else:
            abort(403, message="Validation error")
        
        if user.verify_login_token(args['token']):
            return user
            
        abort(403, message="Validation error")
    
    
# Register views
api.add_resource(LoginUser, '/login', endpoint='user_login')
api.add_resource(UserInfo, '/users/<int:id>', endpoint='user_info')
api.add_resource(UsersAllInfo, '/users/', endpoint='users_all')
api.add_resource(VerifiyUser, '/verify', endpoint='user_verify')