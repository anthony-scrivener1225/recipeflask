from app import db, login_manager
import datetime
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin, current_user
import jwt
from werkzeug.security import check_password_hash, generate_password_hash



# Registers function with flask_login and called when querying info about logged in user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



recipe_history = db.Table('recipe_history',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)


recipe_tags = db.Table(
    'recipe_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)



class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True, index=True)
    pass_hash = db.Column(db.String(256), unique=True)
    confirmed = db.Column(db.Boolean)
    user_recipe_history = db.relationship('Recipe', lazy='subquery', secondary=recipe_history, backref=db.backref('users', lazy=True) )
    

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.pass_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.pass_hash, password)

    def __repr__(self):
        return f'User account: {self.username}.'

    def generate_confirmation_token(self, expiration=3600):
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration)
        payload = {'confirm': self.id,
                    'exp': int(exp.timestamp())
                }
        token = jwt.encode(payload,current_app.config['SECRET_KEY'],algorithm='HS256')
        return token




class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.String(256))
    tags = db.relationship('Tag', secondary=recipe_tags, back_populates='recipes')

    def __repr__(self):
        return f'{self.name}'



class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    recipes = db.relationship('Recipe', secondary=recipe_tags, back_populates='tags')

    def __repr__(self):
        return f'{self.name}'


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(256))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipes = db.relationship('Recipe', backref='ingredients')

    def __repr__(self):
        return f'{self.details}'
