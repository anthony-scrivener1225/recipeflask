from app import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    pass_hash = db.Column(db.String(256), unique=True)
    recipe_history = db.relationship()

    def __init__(self, id, username, pass_hash, recipe_history):
        self.id = id
        self.username = username
        self.pass_hash = pass_hash
        self.recipe_history = recipe_history

    def __repr__(self):
        return f'User account: {self.username}.'

recipe_history = db.Table(
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(1024))
    