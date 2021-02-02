from . import db
from marshmallow import fields, Schema
import datetime


class UserTypeModels(db.Model):
    # table name
    __tablename__ = 'user_type'

    # column
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    user_rel = db.relationship('UserModels', backref='user_type', lazy=True)

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_user_type():
        return UserTypeModels.query.all()

    @staticmethod
    def get_user_type_by_id(id):
        return UserTypeModels.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class UserTypeSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ('id', 'name')
