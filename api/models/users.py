#Local imports
from api import bcrypt
from api.database import db
from api.models.common import BaseModel
from api.common import enums

class User(BaseModel):
    """
    User model
    """

    first_name = db.Column(
        db.String(50),
        nullable=True
    )
    last_name = db.Column(
        db.String(50),
        nullable=True
    )
    username = db.Column(
        db.String(50),
        unique=True,
        nullable=True
    )
    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )
    about = db.Column(
        db.Text(),
        nullable=True
    )
    _password = db.Column(
        db.String(60),
        nullable=False
    )
    status = db.Column(
        db.Enum(enums.Status),
        nullable=False
    )
    role = db.Column(
        db.Enum(enums.Role),
        nullable=False
    )

    def __repr__(self) -> str:
        return (
            f'<User: {self.id}, '
        )

    @property
    def password(self) -> None:
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password: str) -> None:
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self._password, password)
    