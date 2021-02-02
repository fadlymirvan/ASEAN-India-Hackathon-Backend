from . import db, bcrypt, UserTypeSchema
from marshmallow import fields, Schema
import datetime


class UserModels(db.Model):
    # table name
    __tablename__ = 'users'

    # column
    id = db.Column(db.Integer, primary_key=True)
    user_type_id = db.Column(db.Integer, db.ForeignKey('user_type.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    country = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_rel = db.relationship('UserTypeModels', backref='users', lazy=True)

    # class constructor
    def __init__(self, data):
        self.user_type_id = data.get('user_type_id')
        self.name = data.get('name')
        self.email = data.get('email')
        self.country = data.get('country')
        self.password = self.generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            if key == 'password':
                self.password = self.generate_hash(item)
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_user():
        return UserModels.query.all()

    @staticmethod
    def get_user_by_id(id):
        return UserModels.query.get(id)

    @staticmethod
    def get_user_by_email(email):
        return UserModels.query.filter_by(email=email).first()

    def generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    user_type_id = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    country = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_rel = fields.Nested(UserTypeSchema, many=False, only=('name',))
