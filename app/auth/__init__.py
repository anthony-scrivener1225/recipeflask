from flask import Blueprint

blp = Blueprint('auth', __name__)

import app.auth.views