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

user_fields = {
    'uri': fields.Url('user_info'),
    'username': fields.String,
    'email' : fields.String
}

class LoginUser(Resource):
    """ Login the user
    
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str)
    parser.add_argument('password', type=str)
    
    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']
        
        u = User.query.filter_by(username=username).first()
        
        if u.verify_password(password):
            pass
        else:
            pass

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
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('password', type=str)
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
        
        
# Register views
api.add_resource(LoginUser, '/login/', endpoint='user_login')
api.add_resource(UserInfo, '/users/<int:id>', endpoint='user_info')
api.add_resource(UsersAllInfo, '/users/', endpoint='users_all')