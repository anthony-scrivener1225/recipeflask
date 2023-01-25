from flask import Blueprint

blp = Blueprint('recipes', __name__, template_folder='templates/recipes')


from app.recipes.views import views