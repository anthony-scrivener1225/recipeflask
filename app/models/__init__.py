from app import db


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    pass_hash = db.Column(db.String(256), unique=True)
    recipe_history = db.relationship('Recipe', lazy='subquery', secondary=recipe_history, backref=db.backref('users', lazy=True) )

    def __repr__(self):
        return f'User account: {self.username}.'

recipe_history = db.Table('tags',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id'), primary_key=True)
)


recipe_tags = db.Table(
    'recipe_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    description = db.Column(db.String(1024))
    tags = db.relationship('Tag', secondary=recipe_tags, lazy='subquery',
    backref=db.backref('recipes', lazy=True)
    )



class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True)


class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(256))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    recipes = db.relationship('Recipe', backref='ingredients', lazy='dynamic')



