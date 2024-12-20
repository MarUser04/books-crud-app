import { ComponentFixture, TestBed } from '@angular/core/testing';
import { BooksDashboardComponent } from './books-dashboard.component';
import { BookService } from '../../services/book.service';
import { Book } from '../../models/book.model';
import { FormsModule } from '@angular/forms';
import { of } from 'rxjs'; 
describe('BookDashboardComponent', () => {
  let component: BooksDashboardComponent;
  let fixture: ComponentFixture<BooksDashboardComponent>;
  let mockBookService: jasmine.SpyObj<BookService>;

  beforeEach(() => {
    mockBookService = jasmine.createSpyObj('BookService', [
      'getBooks',
      'createBook',
      'updateBook',
      'deleteBook'
    ]);

    mockBookService.getBooks.and.returnValue(of([
      { id: '1', title: 'Book 1', author: 'Author 1', read: false },
      { id: '2', title: 'Book 2', author: 'Author 2', read: true }
    ]));

    mockBookService.createBook.and.returnValue(of({ id: '3', title: 'New Book', author: 'New Author', read: false }));
    mockBookService.updateBook.and.returnValue(of({ id: '1', title: 'Updated Book', author: 'Updated Author', read: false }));
    mockBookService.deleteBook.and.returnValue(of(void 0));

    TestBed.configureTestingModule({
      declarations: [BooksDashboardComponent],
      imports: [FormsModule], 
      providers: [{ provide: BookService, useValue: mockBookService }]
    });

    fixture = TestBed.createComponent(BooksDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize the books array when ngOnInit is called', (done) => {
    component.ngOnInit();
    mockBookService.getBooks().subscribe((data: Book[]) => {
      expect(component.books.length).toBe(2);
      expect(component.books[0].title).toBe('Book 1');
      done();
    });
  });

  it('should call getBooks on ngOnInit', () => {
    component.ngOnInit();
    expect(mockBookService.getBooks).toHaveBeenCalled();
  });

  it('should add a new book when saveNewBook is called', () => {
    const newBook: Book = { title: 'New Book', author: 'New Author', read: false };
    component.newBook = newBook;
    component.saveNewBook();
    
    expect(component.books.length).toBe(2);
    expect(mockBookService.createBook).toHaveBeenCalledWith(newBook);
  });

  it('should disable save button when title or author is empty', () => {
    component.newBook = { title: '', author: '', read: false };
    expect(component.isSaveDisabled()).toBeTrue();
  });

  it('should enable save button when title and author are filled', () => {
    component.newBook = { title: 'Valid Title', author: 'Valid Author', read: false };
    expect(component.isSaveDisabled()).toBeFalse();
  });

  it('should set isEditing to true when editBook is called', () => {
    component.editBook(0);
    expect(component.isEditing[0]).toBeTrue();
  });

  it('should call updateBook when saveBook is called', () => {
    const book: Book = { id: '1', title: 'Updated Book', author: 'Updated Author', read: false };
    component.books = [book];
    component.saveBook(0);
    
    expect(mockBookService.updateBook).toHaveBeenCalledWith(String(book.id), book);
  });

  it('should call deleteBook and refresh the books list', (done) => {
    const bookToDelete: Book = { id: '1', title: 'Book to Delete', author: 'Author', read: false };
    component.books = [bookToDelete];
    component.deleteId = '1';
    
    component.deleteBook();
    mockBookService.deleteBook('1').subscribe(() => {
      expect(mockBookService.getBooks).toHaveBeenCalled();
      done();
    });
  });

  it('should display modal when confirmDelete is called', () => {
    const bookToDelete: Book = { id: '1', title: 'Book to Delete', author: 'Author', read: false };
    component.confirmDelete(bookToDelete);
    expect(component.showModal).toBeTrue();
    expect(component.deleteId).toBe('1');
  });

  it('should close modal when closeModal is called', () => {
    component.closeModal();
    expect(component.showModal).toBeFalse();
    expect(component.deleteId).toBeNull();
  });
});
