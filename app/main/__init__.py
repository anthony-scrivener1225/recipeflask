from flask import Blueprint

blp = Blueprint('main', __name__)

from app.main import views