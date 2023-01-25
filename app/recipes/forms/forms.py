from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from flask_sqlalchemy import SQLAlchemy, session
from app.models import Tag
from app import db


class AddRecipe(FlaskForm):
    
    def __init__(self, choices):
        self.choices = choices
        self.recipe_name = StringField('Name your recipe.', description="Give a succent yet details name for your recipe")
        self.recipe_ingredients = StringField('Ingredients', description="Add the ingredients line by line.", default="1/2 cup Ice, 2 tsp baking soda...")
        self.recipe_tags = SelectMultipleField('Tags',choices=self.choices)
        self.recipe_description = TextAreaField('Provide details about the recipe and why it should be made')
        self.submit = SubmitField('Submit')

class AddTag(FlaskForm):
    tag_name = StringField('Tag name.', description='Short, single word tag name.')
    submit = SubmitField('Submit')