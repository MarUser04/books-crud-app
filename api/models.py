import uuid
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Book model
class Book(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.String(32), primary_key=True, default=lambda: uuid.uuid4().hex)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    read = db.Column(db.Boolean, default=False)

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'read': self.read,
        }
