from flask import Blueprint, jsonify, request
from models import db, Book
from flasgger import swag_from

books_bp = Blueprint('books', __name__)


@books_bp.route('', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'Book created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'title': {'type': 'string'},
                    'author': {'type': 'string'},
                    'read': {'type': 'boolean'}
                }
            }
        },
        400: {
            'description': 'Invalid input'
        }
    },
    'parameters': [
        {
            'name': 'body',
            'description': 'Book object',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'author': {'type': 'string'},
                    'read': {'type': 'boolean'}
                }
            }
        }
    ]
})
def create_book():
    data = request.json
    title = data.get('title')
    author = data.get('author')
    read = data.get('read', False)

    if not title or not author:
        return jsonify({'error': 'Title and author are required'}), 400

    book = Book(title=title, author=author, read=read)
    db.session.add(book)
    db.session.commit()

    return jsonify(book.json()), 201


@books_bp.route('', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of books',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'title': {'type': 'string'},
                        'author': {'type': 'string'},
                        'read': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def get_books():
    books = Book.query.all()
    return jsonify([book.json() for book in books])


@books_bp.route('/<id>', methods=['GET'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'description': 'ID of the book to return',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Book found',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'title': {'type': 'string'},
                    'author': {'type': 'string'},
                    'read': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Book not found'
        }
    }
})
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(book.json())


@books_bp.route('/<id>', methods=['PUT'])
@swag_from({
    'responses': {
        200: {
            'description': 'Book updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'title': {'type': 'string'},
                    'author': {'type': 'string'},
                    'read': {'type': 'boolean'}
                }
            }
        },
        404: {
            'description': 'Book not found'
        },
        400: {
            'description': 'Invalid input'
        }
    },
    'parameters': [
        {
            'name': 'id',
            'description': 'ID of the book to update',
            'in': 'path',
            'type': 'string',
            'required': True
        },
        {
            'name': 'body',
            'description': 'Book object',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'author': {'type': 'string'},
                    'read': {'type': 'boolean'}
                }
            }
        }
    ]
})
def update_book(id):
    data = request.json
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.read = data.get('read', book.read)

    db.session.commit()

    return jsonify(book.json())


@books_bp.route('/<id>', methods=['DELETE'])
@swag_from({
    'parameters': [
        {
            'name': 'id',
            'description': 'ID of the book to delete',
            'in': 'path',
            'type': 'string',
            'required': True
        }
    ],
    'responses': {
        200: {
            'description': 'Book deleted successfully'
        },
        404: {
            'description': 'Book not found'
        }
    }
})
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'})