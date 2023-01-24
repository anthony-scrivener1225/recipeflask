from flask import Blueprint

blp = Blueprint('main', __name__, template_folder='templates/main')

from app.main import views