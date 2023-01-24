from flask import Blueprint

blp = Blueprint('auth', __name__, template_folder='templates/auth')

import app.auth.views