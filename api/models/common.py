# Built-in packages
import time

# Project dependencies
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property

# Local
from api.database import db

class BaseModel(db.Model):
    """Base model """

    __abstract__ = True

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )
    _created_at = db.Column('created_at', db.DateTime(), nullable=False, server_default=func.now())
    _updated_at = db.Column('updated_at', db.DateTime(), nullable=False, server_default=func.now(), onupdate=func.now())

    @hybrid_property
    def created_at(self):
        return self._created_at

    @hybrid_property
    def updated_at(self):
        return self._updated_at