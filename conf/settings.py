import os
from dotenv import load_dotenv

load_dotenv()

BASEDIR = os.path.abspath(os.path.dirname(__file__))

PROJECT = os.getenv('PROJECT')
FLASK_ENV = os.getenv('FLASK_ENV')
FLASK_DEBUG = os.getenv('FLASK_DEBUG')
PORT = os.getenv('PORT')
SECRET_KEY = os.getenv('SECRET_KEY')
SWAGGER_PATH = os.getenv('SWAGGER_PATH')
PROPAGATE_EXCEPTIONS= os.getenv('PROPAGATE_EXCEPTIONS')
PRESERVE_CONTEXT_ON_EXCEPTION= os.getenv('PRESERVE_CONTEXT_ON_EXCEPTION')

# DATABASE
SQLALCHEMY_DATABASE_URI =\
        'sqlite:///' + os.path.join(BASEDIR, os.getenv('DATABASE'))

# OTHER
TOKEN_EXPIRE_MINUTES = os.getenv('TOKEN_EXPIRE_MINUTES')
TOKEN_EXPIRE_HOURS = os.getenv('TOKEN_EXPIRE_HOURS')
