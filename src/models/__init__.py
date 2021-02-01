from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

from .UserTypeModels import UserTypeModels, UserTypeSchema
from .UserModels import UserModels, UserSchema

