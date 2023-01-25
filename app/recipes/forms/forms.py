from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from flask_sqlalchemy import SQLAlchemy, session
from app.models import Tag


class AddRecipe(FlaskForm):
    tag_results = Tag.query.with_entities(Tag.name).all()
    choices = []
    for x in range(tag_results+1):
        choices.append((x+1, tag_results[x]))
    recipe_name = StringField('Name your recipe.', description="Give a succent yet details name for your recipe")
    recipe_ingredients = StringField('Ingredients', description="Use a comma to seperate ingredients.", default="1/2 cup Ice, 2 tsp baking soda...")
    recipe_tags = SelectMultipleField('Tags')
    recipe_description = TextAreaField('Provide details about the recipe and why it should be made')
    submit = SubmitField('Submit')

class AddTag(FlaskForm):
    tag_name = StringField('Tag name.', description='Short, single word tag name.')
    submit = SubmitField('Submit')