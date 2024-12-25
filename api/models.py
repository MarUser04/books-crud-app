import uuid
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    read = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'read': self.read
        }

    @staticmethod
    def schema(many=False):
        class BookSchema(Schema):
            id = fields.Str()
            title = fields.Str(required=True)
            author = fields.Str(required=True)
            read = fields.Bool()

        return BookSchema(many=many)