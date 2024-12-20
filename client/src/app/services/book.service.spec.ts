import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { BookService } from './book.service';
import { Book } from '../models/book.model';

describe('BookService', () => {
  let service: BookService;
  let httpMock: HttpTestingController;

  const dummyBooks: Book[] = [
    { id: '1', title: 'Book 1', author: 'Author 1', read: false },
    { id: '2', title: 'Book 2', author: 'Author 2', read: true }
  ];

  const newBook: Book = { id: '3', title: 'Book 3', author: 'Author 3', read: false };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [BookService]
    });

    service = TestBed.inject(BookService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should retrieve books from the API via GET', () => {
    service.getBooks().subscribe(books => {
      expect(books.length).toBe(2);
      expect(books).toEqual(dummyBooks);
    });

    const req = httpMock.expectOne('http://localhost:5000/books');
    expect(req.request.method).toBe('GET');
    req.flush(dummyBooks);
  });

  it('should create a book via POST', () => {
    service.createBook(newBook).subscribe(book => {
      expect(book).toEqual(newBook);
    });

    const req = httpMock.expectOne('http://localhost:5000/books');
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(newBook);
    req.flush(newBook);
  });

  it('should update a book via PUT', () => {
    const updatedBook: Book = { id: '3', title: 'Updated Book 3', author: 'Updated Author 3', read: true };

    service.updateBook('3', updatedBook).subscribe(book => {
      expect(book).toEqual(updatedBook);
    });

    const req = httpMock.expectOne('http://localhost:5000/books/3');
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual(updatedBook);
    req.flush(updatedBook);
  });

  it('should delete a book via DELETE', () => {
    service.deleteBook('3').subscribe();

    const req = httpMock.expectOne('http://localhost:5000/books/3');
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });
});
