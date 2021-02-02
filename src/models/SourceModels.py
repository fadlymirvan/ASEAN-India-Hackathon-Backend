from . import db
from marshmallow import fields, Schema
import datetime


class SourceModels(db.Model):
    # table name
    __tablename__ = 'source'

    # column
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    data_rel = db.relationship('DataModels', backref='source', lazy=True)

    # class constructor
    def __init__(self, data):
        self.name = data.get('name')
        self.type = data.get('type')
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
    def get_all_source():
        return SourceModels.query.all()

    @staticmethod
    def get_source_by_id(id):
        return SourceModels.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class SourceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        fields = ('id', 'name', 'type', 'created_at', 'updated_at')
