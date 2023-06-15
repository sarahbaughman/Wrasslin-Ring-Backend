#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Api, Resource

# Local imports
from config import app, db, api

from models import User, Match, MatchWrestler, Show, Promotion, ProposedMatch, ProposedMatchWrestler, UserPromotion, UserShow

# Views go here!
api = Api(app)



@app.before_request
def check_if_logged_in():
    open_access_list = [
        'login',
        'logout',
        'check_session'
    ]

    if (request.endpoint) not in open_access_list and (not session.get('user_id')):
        return {'error': '401 Unauthorized'}, 401

class CheckSession(Resource):

    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session.get('user_id')).first()
            return user.to_dict(), 200

        return {'error': '401: Not Authorized'}, 401
        

api.add_resource(CheckSession, '/check_session')


class Login(Resource):

    def post(self):
        user_input = request.get_json()
        username = user_input.get('username')
        password = user_input.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200
        return {'error': '401 Unauthorized'}, 401
    
api.add_resource(Login, '/login' )



class Logout(Resource):
    def delete(self): 
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {'error': '204: 401 Unauthorized'}, 204

api.add_resource(Logout, '/logout')


# class MemberOnlyIndex(Resource):
    
#     def get(self):
    
#         articles = Article.query.filter(Article.is_member_only == True).all()
#         return [article.to_dict() for article in articles], 200
# Inspiration for promoter vs wrestler access

if __name__ == '__main__':
    app.run(port=5555, debug=True)
