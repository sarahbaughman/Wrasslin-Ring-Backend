import re
from flask import Flask, abort
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.ext.hybrid import hybrid_property
from config import db, bcrypt




# Models

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-match_wrestlers.user', 
                        '-matches.users', 
                        '-proposed_match_wrestlers.user', 
                        '-proposed_matches.users', 
                        '-promotions.users',
                        '-shows.users',
                        )

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    regions = db.Column(db.String)
    weight = db.Column(db.Integer)
    phone = db.Column(db.String)
    email = db.Column(db.String, nullable = False)
    image = db.Column(db.String)
    instagram = db.Column(db.String)
    payment = db.Column(db.String)
    username = db.Column(db.String, nullable = False)
    _password_hash = db.Column(db.String)
    role = db.Column(db.String, default = 'wrestler')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    match_wrestlers = db.relationship('MatchWrestler', back_populates = 'user')
    matches = association_proxy('match_wrestlers', 'match', creator=lambda m: MatchWrestler(match = m))
    
    proposed_match_wrestlers = db.relationship('ProposedMatchWrestler', back_populates = 'user')
    proposed_matches = association_proxy('proposed_match_wrestlers', 'proposed_match', creator=lambda pm: ProposedMatchWrestler(proposed_match = pm) )

    def __repr__(self):
        return f'User {self.id} : {self.name}'
    

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')


    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    # @validates('name')
    # def validate_name(self, attr, name):
    #     if type(name) is str and name and len(name) >= 1: 
    #         return name
    #     else:
    #         abort(422, "Name must be entered and be a string of at least 1 character in length. Please try again.")
    
    # @validates('regions')
    # def validate_regions(self, attr, regions):
    #     if type(regions) is str and len(regions) >= 1: 
    #         return regions
    #     else:
    #         abort(422, "Regions must be a string of at least 1 character in length. Please try again.")
    
    # @validates('weight')
    # def validate_weight(self, attr, weight):
    #     if 2 <= len(str(weight)) <= 3 : 
    #         return weight
    #     else:
    #         abort(422, "Weight must be an integer either 2 or 3 digits long. Please try again.")
    
    # @validates('phone')
    # def validate_phone(self, attr, phone):
    #     if 15 <= len(phone) <= 12: 
    #         return phone
    #     else:
    #         abort(422, "Phone number must be written in the following format: +1-xxx-xxx-xxxx. Please try again.")
    
    # @validates('email')
    # def validate_email(self, attr, email):
    #     if '@' not in email or '.' not in email:
    #         abort(422, "Email must be in the following format: youremail@somemail.com . Please try again.")
    #     else:
    #         return email
    
    # @validates('instagram')
    # def validate_instagram(self, attr, instagram):
    #     pattern = r'^[a-zA-Z0-9@_.]+$'

    #     if not re.match(pattern, instagram) or not len(instagram) <= 30:
    #         abort(422, "Instagram handle must be in the following format: @username, using only numbers, letters, underscores and periods. Please try again.")
    #     else:
    #         return instagram
    
    # @validates('payment')
    # def validate_payment(self, attr, payment):
    #     if type(payment) is str and 8 <= len(payment) <=30 :
    #         return payment
    #     else:
    #         abort(422, "Payment method must be a string and written in the following format: Venmo: Username or Cashapp: Username, etc. Please try again.")




class Match(db.Model, SerializerMixin):
    __tablename__ = 'matches'

    serialize_rules = ('-show.matches', 
                        '-match_wrestlers.match', 
                        '-users.matches',
                        )

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String, nullable = True)
    storyline = db.Column(db.String)
       # accepted = db.Column(db.String, default = False, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable = True)
    show = db.relationship('Show', back_populates = 'matches')

    match_wrestlers = db.relationship('MatchWrestler', back_populates = 'match')
    users = association_proxy('match_wrestlers', 'user', creator=lambda u: MatchWrestler(user = u))

    def __repr__(self):
        return f'Match {self.id}'

class MatchWrestler(db.Model, SerializerMixin):
    __tablename__ = 'match_wrestlers'

    serialize_rules = ('-match.match_wrestlers', 
                        '-user.match_wrestlers',
                        )

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    match = db.relationship('Match', back_populates = 'match_wrestlers')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates = 'match_wrestlers')

    def __repr__(self):
        return f'MatchWrestler {self.id}'

class Show(db.Model, SerializerMixin):
    __tablename__ = 'shows'

    serialize_rules = ('-promotion.shows', 
                        '-matches.show', 
                        '-users.shows',
                        ) 

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    venue = db.Column(db.String, nullable = False)
    address = db.Column(db.String)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    date = db.Column(db.Date, nullable=True)
    where_to_view = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))
    promotion = db.relationship('Promotion', back_populates = 'shows')

    matches = db.relationship('Match', back_populates = 'show')

    def __repr__(self):
        return f'Show {self.id} : {self.name}'
    
    # @validates('name')
    # def validate_name(self, attrr, name):
    #     existing_show = Show.query.filter_by(name=name, promotion_id=self.promotion_id).first()
    #     if existing_show is not None and existing_show.id != self.id:
    #         abort("Name must exist and be unique within the promotion")
    #     return name
    
    # @validates('venue')
    # def validate_venue(self, attr, venue):
    #     if type(venue) is str and len(venue) >= 1 and venue:
    #         return venue 
    #     else: 
    #         abort(422, 'Show must have a venue, venue must be a string greater than 1 character. Please try again.')

    # @validates('address')
    # def validate_address(self, attr, address):
    #     if type(address) is str and 45 >= len(address) >= 4:
    #         return address
    #     else: 
    #         abort(422, 'Address must be a string between 4 and 45 characters. Please try again.')

    # @validates('city')
    # def validate_city(self, attr, city):
    #     if type(city) is str and 50 >= len(city) >= 1 :
    #         return city
    #     else: 
    #         abort(422, 'City must be a string between 1 and 50 characters. Please try again.')






    # state 
    # date 
    # where_to_view 

class Promotion(db.Model, SerializerMixin):
    __tablename__ = 'promotions'

    serialize_rules = ('-proposed_matches.promotion', 
                       '-shows.promotion', 
                       '-users.promotions',
                       )
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    # promoter = db.Column(db.?) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    proposed_matches = db.relationship('ProposedMatch', back_populates = 'promotion', cascade = 'all, delete-orphan')
    # not deleting orphans because I want the record of matches that have happened to remain for 
    # wrestler history to still be intact 

    shows = db.relationship('Show', back_populates = 'promotion')
    
    def __repr__(self):
        return f'Promotion {self.id} : {self.name}'
    
    # @validates('name')
    # def validate_name(self, key, name):
    #     existing_promotion = Promotion.query.filter(Promotion.name == name).first()
    #     if existing_promotion is not None and existing_promotion.id != self.id:
    #         raise ValueError("Name must be unique")
    #     return name



class ProposedMatch(db.Model, SerializerMixin):
    __tablename__ = 'proposed_matches'

    serialize_rules = ('-promtion.proposed_matches', 
                        '-users.proposed_matches', 
                        '-proposed_match_wrestlers.proposed_match',
                        )

    id = db.Column(db.Integer, primary_key = True)
    storyline = db.Column(db.String)
    type = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))
    promotion = db.relationship('Promotion', back_populates = 'proposed_matches')

    proposed_match_wrestlers = db.relationship('ProposedMatchWrestler', back_populates = 'proposed_match', cascade = 'all, delete-orphan')
    users = association_proxy('proposed_match_wrestlers', 'user', creator=lambda u: ProposedMatchWrestler(user = u) )

    def __repr__(self):
        return f'ProposedMatch {self.id}'
    
    # @validates('storyline')
    # def validate_storyline(self, attr, storyline):
    #     if type(storyline) is str and len(storyline) > 0:
    #         return storyline
    #     else: 
    #         abort(422, 'Storyline must be a string greater than 0 characters, if no storyline write N/A. Please try again.')
        
    # @validates('type')
    # def validate_type(self, attr, type):
    #     if type(type) is str and len(type) > 5:
    #         return type
    #     else: 
    #         abort(422, 'Match type must be a string greater than 5 characters. Please try again.' )
    
    # @validates('promotion_id')
    # def validate_user_id(self, attr, promotion_id):
    #     promotion = Promotion.query.filter(Promotion.id == promotion_id).first()
    #     if type(promotion) is int and promotion:
    #         return promotion_id
    #     else:
    #         abort(422, 'Invalid data, promotion does not exist. Please try again.')

class ProposedMatchWrestler(db.Model, SerializerMixin):
    __tablename__ = 'proposed_match_wrestlers'

    serialize_rules =  ('-user.proposed_match_wrestlers', 
                        '-proposed_match.proposed_match_wrestlers',
                        )

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    proposed_match_id = db.Column(db.Integer, db.ForeignKey('proposed_matches.id'))
    proposed_match = db.relationship('ProposedMatch', back_populates = 'proposed_match_wrestlers')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates = 'proposed_match_wrestlers')

    def __repr__(self):
        return f'ProposedMatchWrestler {self.id}'
    
    # @validates('user_id')
    # def validate_user_id(self, attr, user_id):
    #     user = User.query.filter(User.id == user_id).first()
    #     if type(user_id) is int and user:
    #         return user_id
    #     else:
    #         abort(422, 'Invalid data, user does not exist. Please try again.')
        
    
    # @validates('proposed_match_id')
    # def validate_user_id(self, attr, proposed_match_id):
    #     proposed_match = ProposedMatch.query.filter(ProposedMatch.id == proposed_match_id).first()
    #     if type(proposed_match_id) is int and proposed_match:
    #         return proposed_match
    #     else:
    #         abort(422, 'Invalid data, proposed match does not exist. Please try again.')
        





