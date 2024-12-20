import pytest
from app import app
from models import db, Book

@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client 
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_create_book_success(test_client):
    response = test_client.post('/books', json={
        'title': 'Test Book',
        'author': 'Test Author',
        'read': True
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Test Book'
    assert data['author'] == 'Test Author'
    assert data['read'] is True

def test_create_book_missing_fields(test_client):
    response = test_client.post('/books', json={'title': 'Test Book'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_get_books_empty(test_client):
    response = test_client.get('/books')
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_get_books_non_empty(test_client):
    book = Book(title='Test Book', author='Test Author', read=True)
    with test_client.application.app_context():
        db.session.add(book)
        db.session.commit()

    response = test_client.get('/books')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Book'

def test_get_book_success(test_client):
    book = Book(title='Test Book', author='Test Author', read=True)
    with test_client.application.app_context():
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = test_client.get(f'/books/{book_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Test Book'

def test_get_book_not_found(test_client):
    response = test_client.get('/books/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_update_book_success(test_client):
    book = Book(title='Old Title', author='Old Author', read=False)
    with test_client.application.app_context():
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = test_client.put(f'/books/{book_id}', json={
        'title': 'New Title',
        'author': 'New Author',
        'read': True
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'New Title'

def test_update_book_not_found(test_client):
    response = test_client.put('/books/999', json={'title': 'New Title'})
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data

def test_delete_book_success(test_client):
    book = Book(title='Test Book', author='Test Author', read=True)
    with test_client.application.app_context():
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = test_client.delete(f'/books/{book_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert 'message' in data

def test_delete_book_not_found(test_client):
    response = test_client.delete('/books/999')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
