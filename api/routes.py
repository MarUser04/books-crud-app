from flask import Blueprint, jsonify, request
from models import db, Book

books_bp = Blueprint('books', __name__)

# Create a book (POST /books)
@books_bp.route('', methods=['POST'])
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

    return jsonify(book.to_dict()), 201

# Get all books (GET /books)
@books_bp.route('', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])

# Get a single book by ID (GET /books/<id>)
@books_bp.route('/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    return jsonify(book.to_dict())

# Update a book by ID (PUT /books/<id>)
@books_bp.route('/<id>', methods=['PUT'])
def update_book(id):
    data = request.json
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.read = data.get('read', book.read)

    db.session.commit()

    return jsonify(book.to_dict())

# Delete a book by ID (DELETE /books/<id>)
@books_bp.route('/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'})
