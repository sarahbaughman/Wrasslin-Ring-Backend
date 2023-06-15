from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from config import db
# bcrypt

# Models



class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    # serializer 

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    regions = db.Column(db.String)
    weight = db.Column(db.String, nullable = False)
    phone = db.Column(db.String)
    email = db.Column(db.String, nullable = False)
    instagram = db.Column(db.String)
    payment = db.Column(db.String)
    # role = db.Column(db.String, default = 'wrestler')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    match_wrestlers = db.relationship('MatchWrestler', back_populates = 'user')
    matches = association_proxy('match_wrestlers', 'match', creator=lambda m: MatchWrestler(match = m))
    
    proposed_match_wrestlers = db.relationship('ProposedMatchWrestler', back_populates = 'user')
    proposed_matches = association_proxy('proposed_match_wrestlers', 'proposed_match', creator=lambda pm: ProposedMatchWrestler(proposed_match = pm) )

    user_promotions = db.relationship('UserPromotion', back_populates = 'user')
    promotions = association_proxy('user_promotions', 'promotion',creator=lambda p: UserPromotion(promotion = p))


    def __repr__(self):
        return f'User {self.id} : {self.name}'

class Match(db.Model, SerializerMixin):
    __tablename__ = 'matches'

    # serializer 

    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.String, nullable = True)
    storyline = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'))
    show = db.relationship('Show', back_populates = 'matches')

    match_wrestlers = db.relationship('MatchWrestler', back_populates = 'match')
    users = association_proxy('match_wrestlers', 'user', creator=lambda u: MatchWrestler(user = u))

    def __repr__(self):
        return f'Match {self.id}'

class MatchWrestler(db.Model, SerializerMixin):
    __tablename__ = 'match_wrestlers'

    # serializer 

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

    # serializer 

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    venue = db.Column(db.String, nullable = False)
    address = db.Column(db.String)
    city = db.Column(db.String, nullable = False)
    state = db.Column(db.String, nullable = False)
    date = db.Column(db.DateTime, nullable=True)
    where_to_view = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))
    promotion = db.relationship('Promotion', back_populates = 'shows')

    matches = db.relationship('Match', back_populates = 'show')

    def __repr__(self):
        return f'Show {self.id} : {self.name}'

class Promotion(db.Model, SerializerMixin):
    __tablename__ = 'promotions'

    # serializer 

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    # promoter = db.Column(db.?) //need to figure this out __________________________
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    proposed_matches = db.relationship('ProposedMatch', back_populates = 'promotion', cascade = 'all, delete-orphan')
    # not deleting orphans because I want the record of matches that have happened to remain for 
    # wrestler history to still be intact 

    shows = db.relationship('Show', back_populates = 'promotion')

    user_promotions = db.relationship('UserPromotion', back_populates = 'promotion')
    users = association_proxy('user_promotions', 'user',creator=lambda u: UserPromotion(user = u))

    def __repr__(self):
        return f'Promotion {self.id} : {self.name}'


class ProposedMatch(db.Model, SerializerMixin):
    __tablename__ = 'proposed_matches'

    # serializer 

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


class ProposedMatchWrestler(db.Model, SerializerMixin):
    __tablename__ = 'proposed_match_wrestlers'

    # serializer 

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    proposed_match_id = db.Column(db.Integer, db.ForeignKey('proposed_matches.id'))
    proposed_match = db.relationship('ProposedMatch', back_populates = 'proposed_match_wrestlers')

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates = 'proposed_match_wrestlers')

    def __repr__(self):
        return f'ProposedMatchWrestler {self.id}'


class UserPromotion(db.Model, SerializerMixin):
    __tablename__ = 'user_promotions'

    # serializer 

    id = db.Column(db.Integer, primary_key = True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    promotion_id = db.Column(db.Integer, db.ForeignKey('promotions.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    promotion = db.relationship('Promotion', back_populates = 'user_promotions')
    user = db.relationship('User', back_populates = 'user_promotions')

    def __repr__(self):
        return f'ProposedMatchWrestler {self.id}'

