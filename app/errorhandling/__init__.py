from flask import Blueprint


blp = Blueprint('errorhandling', __name__, template_folder="templates/errorhandling",url_prefix='/error',static_url_path='static/errorhandling')

from app.errorhandling.views import views