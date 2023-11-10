from enum import Enum

class Status(Enum):
    PENDING = 'pending'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class Role(Enum):
    ADMIN = 'admin'
    USER = 'user'
