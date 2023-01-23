from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True)
    pass_hash = db.Column(db.String(256), unique=True)

class RecipeHistory(db.Model)