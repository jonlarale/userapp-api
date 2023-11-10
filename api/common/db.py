# Python libraries
from typing import Any

# Local modules
from api.database import db
from api.models import *


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        

def db_cleanup(arg: Any) -> None:
    """Remove pending transactions and close connection to the database."""
    
    db.session.rollback()   # Won´t do anything if there are no pending transactions.
    
    db.session.close()
    db.session.remove()
    db.get_engine().dispose()