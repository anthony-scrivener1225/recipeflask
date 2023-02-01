from flask import Blueprint

blp = Blueprint('auth', __name__,template_folder='templates/auth',url_prefix='/auth')

import app.auth.views