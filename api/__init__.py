import os

# Project dependencies
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
bcrypt = Bcrypt()
cors = CORS()

# Local modules
from conf import cfg
from api.common.db import init_db

authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

root_api = Api(doc=cfg.SWAGGER_PATH, security='BearerAuth', authorizations=authorizations)


def create_api():
   
    app = Flask(__name__)
    app.config.from_mapping(vars(cfg))
    cors.init_app(app)
    init_db(app)
    bcrypt.init_app(app)
    root_api.init_app(app)

    root_api.version = "0.0.1"
    root_api.title = "USERAPP API"
    root_api.description="""
<p>API for the users app</p>

"""
    from api.routes.users import users_ns
    from api.routes.auth import auth_ns

    root_api.add_namespace(users_ns)
    root_api.add_namespace(auth_ns)

    return app
