from app import app_factory
from os import getenv, path
from dotenv import load_dotenv
from config import basedir

if path.exists(basedir + '.env'):
    load_dotenv(path.join(basedir + '.env'))

app = app_factory(getenv('ENV') or 'default')



if __name__ == '__main__':
    app.run(DEBUG=app.config['DEBUG'], port=app.config['PORT'])