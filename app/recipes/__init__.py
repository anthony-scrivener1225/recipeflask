from flask import Blueprint

blp = Blueprint('recipes', __name__, template_folder='templates/recipes',url_prefix='/recipes',static_folder='static/recipes')


from app.recipes.views import views