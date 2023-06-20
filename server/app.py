#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Api, Resource
import datetime
from sqlalchemy.exc import IntegrityError

# Local imports
from config import app, db, api
from models import User, Match, MatchWrestler, Show, Promotion, ProposedMatch, ProposedMatchWrestler

# Views go here!
api = Api(app)



# @app.before_request
# def check_if_logged_in():
#     open_access_list = [
#         'login',
#         'logout',
#         'check_session'
#     ]

#     if (request.endpoint) not in open_access_list and (not session.get('user_id')):
#         return {'error': '401 Unauthorized'}, 401


class ClearSession(Resource):

    def delete(self):
    
        session['user_id'] = None

        return {}, 204
    
api.add_resource(ClearSession, '/clear', endpoint='clear')

class Signup(Resource):
    def post (self):

        username = request.get_json()['username']
        password = request.get_json()['password']

        if username and password:

            user_input = request.get_json()
            
            new_user = User(
                name = user_input.get('name'),
                regions = user_input.get('regions'),
                weight = user_input.get('weight'),
                phone = user_input.get('phone'),
                email = user_input.get('email'),
                instagram = user_input.get('instagram'),
                payment = user_input.get('payment'),
                role = user_input.get('role'),
                username = username,
            )
            new_user.password_hash = password
            try: 
                db.session.add(new_user)
                db.session.commit()

                session['user_id'] = new_user.id
                session['role'] = new_user.role

                user_response = {
                    "id" : new_user.id,
                    "name" : new_user.name,
                    "regions" : new_user.regions,
                    "weight" : new_user.weight,
                    "phone" : new_user.phone,
                    "email" : new_user.email,
                    "instagram" : new_user.instagram,
                    "payment" : new_user.payment,
                    "username" : new_user.username,
                    'role' : new_user.role,
                }

                return user_response, 201
            
            except IntegrityError: 

                return {'error' : '422 Unprocessable Entity, cannot create account. Please try again.'}, 422

api.add_resource(Signup, '/signup', endpoint='signup')


class CheckSession(Resource):

    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session.get('user_id')).first()
            return user.to_dict(), 200

        return {'error': '401: Not Authorized'}, 401
        

api.add_resource(CheckSession, '/check_session')


class Login(Resource):

    def post(self):
        username = request.get_json()['username']
        password = request.get_json()['password']
        

        user = User.query.filter(User.username.like(username)).first()
        
        if user:
            if user.authenticate(password):
            
                session['user_id'] = user.id
                session['role'] = user.role

                user_response = {
                "id" : user.id,
                "name" : user.name,
                "regions" : user.regions,
                "weight" : user.weight,
                "phone" : user.phone,
                "email" : user.email,
                "instagram" : user.instagram,
                "payment" : user.payment,
                "username" : user.username,
                "role" : user.role,
                }
                return user_response, 200
        
        return {'error': ['Username or password invalid. Please try again.']}, 401
    
api.add_resource(Login, '/login', endpoint = 'login' )



class Logout(Resource):
    def delete(self): 
        if session.get('user_id'):
            session['user_id'] = None
            session['role'] = None
            return {}, 204
        return {'error': '204: 401 Unauthorized'}, 204

api.add_resource(Logout, '/logout', endpoint='logout')

class Users(Resource):
    def get (self):
        users = User.query.filter_by(role='wrestler').all()
        users_dict = [u.to_dict(only = ('id', 'name','regions', 'weight', 'phone', 'email', 'instagram', 'payment', 'username', 'role',)) for u in users]

        return users_dict, 200

api.add_resource(Users, '/users')

class Matches(Resource):
    def get(self):
        matches = Match.query.all()
        matches_dict = [m.to_dict(only = ('storyline', 'type', 'show.name', 'match_wrestlers.user.name', 'match_wrestlers.user.id')) for m in matches]

        return matches_dict, 200
    
    def post(self):
        if session.get('user_id') and session.get('role') == 'promoter':
            user_input = request.get_json()
            new_match = Match(
                type = user_input['type'],
                storyline = user_input['storyline'],
                show_id = user_input['show_id'],
            )
            
            db.session.add(new_match)
            db.session.commit()

            new_match_response = {
                    "type" : new_match.type,
                    "storyline" : new_match.storyline,
                    "show_id" : new_match.show_id,
            }

            return new_match_response, 201
        
        return {'error': '401 User not authorized to view this content. Please try again.'}, 401

api.add_resource(Matches,'/matches', endpoint = 'matches')

class MatchById(Resource):
    def get(self, id):
        match = Match.query.filter(Match.id == id).first()
        if match:
            return match.to_dict(only = ('storyline', 'type', 'show.name', 'match_wrestlers.user.name', 'match_wrestlers.user.id')), 200
        else:
            return {'error': 'Match not found. Please try again.'}, 404

    def patch(self, id):
        
        match = Match.query.filter(Match.id == id).first()
        if session.get('user_id') and session.get('role') == 'promoter':
            if match:
                for attr in request.get_json():
                    setattr(match, attr, request.get_json()[attr])
                db.session.add(match)
                db.session.commit()
                return match.to_dict(only = ('storyline', 'type', 'show.name', 'match_wrestlers.user.name', 'match_wrestlers.user.id')), 200
            
            else:
                return {'error': 'Match not found. Please try again.'}, 404
            
        return {'error': '401 User not authorized to view this content. Please try again.'}, 401
    
    def delete(self,id):
        match = Match.query.filter(Match.id == id).first()
        if session.get('user_id') and session.get('role') == 'promoter':
            if match:
                db.session.delete(match)
                db.session.commit()
                return {}, 204
            
            else:
                return {'error': 'Match not found. Please try again.'}, 404
            
        return {'error': '401 User not authorized to view this content. Please try again.'}, 401

api.add_resource(MatchById,'/matches/<int:id>', endpoint = 'matches/<int:id>')


class Shows(Resource):
    def get(self):
        
        shows = Show.query.all()
        shows_dict = [s.to_dict(only=('id', 'name', 'venue', 'address', 'city', 'state', 'date', 'where_to_view',)) for s in shows]

        return shows_dict, 200
    
    
    def post(self):
        if session.get('user_id') and session.get('role') == 'promoter':
            user_input = request.get_json()
            date_str = user_input['date']

            date_object = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()

            new_show = Show(
                name = user_input['name'],
                venue = user_input['venue'],
                address = user_input['address'],
                city = user_input['city'],
                state = user_input['state'],
                date = date_object,
                where_to_view = user_input['where_to_view'],
            )

            db.session.add(new_show)
            db.session.commit()

            return new_show.to_dict(), 201
        
        return {'error': '401 User not authorized to view this content. Please try again.'}, 401

api.add_resource(Shows,'/shows', endpoint = 'shows')

class ShowById(Resource):
    def get(self, id):
        show = Show.query.filter(Show.id == id).first()
        if show:
            return show.to_dict(only=('id', 'name', 'venue', 'address', 'city', 'state', 'date', 'where_to_view',))
        else:
            return {'error': 'Show not found. Please try again.'}, 404
    
    
    def patch(self, id):
        show = Show.query.filter(Show.id == id).first()
    
        if session.get('user_id') and session.get('role') == 'promoter':
            if show:
                user_input = request.get_json()
                date_str = user_input.get('date')
                
                if date_str:
                    date_object = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                    setattr(show, 'date', date_object)
                
                for attr in user_input:
                    if attr != 'date':
                        setattr(show, attr, user_input[attr])
                db.session.add(show)
                db.session.commit()

                return show.to_dict(only=('id', 'name', 'venue', 'address', 'city', 'state', 'date', 'where_to_view',)), 200
           
            else:
                return {'error': 'Show not found. Please try again.'}, 404
        else: 
            return {'error' : 'Unauthorized, only a promoter can edit and delete shows.'}, 401
    
    def delete(self,id):
        show = Show.query.filter(Show.id == id).first()
        if session.get('user_id') and session.get('role') == 'promoter':
            if show:
                db.session.delete(show)
                db.session.commit()
                return {}, 204
            
            else:
                return {'error': 'Show not found. Please try again.'}, 404
        else: 
            return {'error' : 'Unauthorized, only a promoter can edit and delete shows.'}, 401

api.add_resource(ShowById,'/shows/<int:id>', endpoint = 'shows/<int:id>')


class Promotions(Resource):
    def get(self):
        promotions = Promotion.query.all()
        promotions_dict = [p.to_dict(only = ('name', 'id', 'shows.name')) for p in promotions] 

        return promotions_dict, 200
    
    def post(self):
        user_input = request.get_json()
        
        new_promotion = Promotion(
            name = user_input['name']
        )

        db.session.add(new_promotion)
        db.session.commit()

        new_promotion_response = {
            "name" : new_promotion.name,
            "id" : new_promotion.id,
            "shows" : new_promotion.shows
        }

        return new_promotion_response, 201
    

api.add_resource(Promotions, '/promotions', endpoint = '/promotions')


class PromotionById(Resource):
    def get(self, id):
        promotion = Promotion.query.filter(Promotion.id == id).first()
        
        if promotion:
            return promotion.to_dict(only = ('name','id', 'shows.name')), 200
        else:
            return {'error': 'Promotion not found. Please try again.'}, 404
    
    def patch(self, id):
        promotion = Promotion.query.filter(Promotion.id == id).first()
        if promotion:
            for attr in request.get_json():
                setattr(promotion, attr, request.get_json()[attr])
            db.session.add(promotion)
            db.session.commit()

            return promotion.to_dict(only = ('name','id', 'shows.name')), 200
        else:
            return {'error': 'Promotion not found. Please try again.'}, 404
    
    def delete(self,id):
        promotion = Promotion.query.filter(Promotion.id == id).first()
        if promotion:
            db.session.delete(promotion)
            db.session.commit()
            return {}, 204
        else:
            return {'error': 'Promotion not found. Please try again.'}, 404

api.add_resource(PromotionById,'/promotions/<int:id>', endpoint = '/promotions/<int:id>')


# class ProposedMatches(Resource):
#     def get(self):
#         proposed_matches = ProposedMatch.query.all()
#         proposed_matches_dict = [pm.to_dict for pm in proposed_matches] 

#         return proposed_matches_dict, 200
    
#     def post(self):
#         user_input = request.get_json()
#         new_proposed_match = ProposedMatch(
#             storyline = user_input['storyline'],
#             type = user_input['type'],
#             promotion_id = user_input['promotion_id'],

#         )

#         db.session.add(new_proposed_match)
#         db.session.commit()

#         return new_proposed_match.to_dict, 201

# api.add_resource(ProposedMatches, '/proposedmatches', endpoint = '/proposedmatches')


# class ProposedMatchById(Resource):
#     def get(self, id):
#         proposed_match = ProposedMatch.query.filter(ProposedMatch.id == id).first()
        
#         if proposed_match:
#             return proposed_match, 200
        
#         else:
#             return {'error': 'Proposed match not found. Please try again.'}, 404
    
#     def patch(self, id):
#         proposed_match = ProposedMatch.query.filter(ProposedMatch.id == id).first()

#         if proposed_match: 
#             for attr in request.get_json():
#                 setattr(proposed_match, attr, request.get_json[attr])
#             db.session.add(proposed_match)
#             db.session.commit()

#             return proposed_match.to_dict(), 200
#         else:
#             return {'error': 'Proposed match not found. Please try again.'}, 404
    
#     def delete(self,id):
#         proposed_match = ProposedMatch.query.filter(ProposedMatch.id == id).first()
#         if proposed_match:
#             db.session.delete(proposed_match)
#             db.session.commit()
#             return {}, 204
        
#         else:
#             return {'error': 'Proposed match not found. Please try again.'}, 404

# api.add_resource(ProposedMatchById, '/proposedmatches/<int:id>', endpoint = '/proposedmatches/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
