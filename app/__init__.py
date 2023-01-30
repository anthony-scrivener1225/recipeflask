from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config
from flask_login import LoginManager



db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def app_factory(configurations):
    app = Flask(__name__)

    app.config.from_object(config[configurations])
    
    db.init_app(app)
    login_manager.init_app(app)

    Migrate(app=app, db=db)
#   Blueprint imports
    from app.main import blp as main_blp
    app.register_blueprint(main_blp)
    from app.auth import blp as auth_blp
    app.register_blueprint(auth_blp)
    from app.recipes import blp as recipe_blp
    app.register_blueprint(recipe_blp)


    
    return app
