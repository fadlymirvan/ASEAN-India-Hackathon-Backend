from . import db, SourceSchema
from marshmallow import fields, Schema
import datetime


class DataModels(db.Model):
    # table name
    __tablename__ = 'data'

    # column
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id', ondelete='CASCADE'), nullable=False)
    lat = db.Column(db.Text, nullable=False)
    long = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.Text, nullable=False)
    fishing_hours = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    source_rel = db.relationship('SourceModels', backref='data', lazy=True)

    # class constructor
    def __init__(self, data):
        self.lat = data.get('lat')
        self.long = data.get('long')
        self.source_id = data.get('source_id')
        self.frequency = data.get('frequency')
        self.fishing_hours = data.get('fishing_hours')
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
    def get_all_data():
        return DataModels.query.all()

    @staticmethod
    def get_data_by_id(id):
        return DataModels.query.get(id)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class DataSchema(Schema):
    id = fields.Int(dump_only=True)
    source_id = fields.Int(required=True)
    lat = fields.Str(required=True)
    long = fields.Str(required=True)
    frequency = fields.Str(required=True)
    fishing_hours = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    source_rel = fields.Nested(SourceSchema, many=False, only=('name', 'type'))
