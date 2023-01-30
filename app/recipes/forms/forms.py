from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField,FieldList,FormField
from flask_sqlalchemy import SQLAlchemy, session
from app.models import Tag
from app import db
from wtforms_sqlalchemy.fields import QuerySelectMultipleField




class IngredientForm(FlaskForm):
    ingredient = StringField(label="Recipe Ingredients!")

class AddRecipe(FlaskForm):
    def tag_collector():
        return db.session.query(Tag).all()
    recipe_name = StringField('Name your recipe.', description="Give a succent yet details name for your recipe")
    recipe_ingredients = FieldList(FormField(IngredientForm))
    recipe_tags = QuerySelectMultipleField(query_factory=tag_collector)
    recipe_description = TextAreaField('Provide details about the recipe and why it should be made')
    submit = SubmitField('Submit')

class AddTag(FlaskForm):
    tag_name = StringField('Tag name.', description='Short, single word tag name.')
    submit = SubmitField('Submit')