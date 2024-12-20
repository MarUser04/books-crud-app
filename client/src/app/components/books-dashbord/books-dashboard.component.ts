import { Component, OnInit } from '@angular/core';
import { BookService } from '../../services/book.service';
import { Book } from '../../models/book.model';	

@Component({
  standalone: false,
  selector: 'app-books-dashboard',
  templateUrl: './books-dashboard.component.html',
  styleUrl: './books-dashboard.component.css'
})
export class BooksDashboardComponent implements OnInit {
  books: Book[] = [];
  isEditing: boolean[] = [];
  showModal: boolean = false;
  deleteId: string | null = null;
  addingNewBook: boolean = false;
  newBook: Book = { id: '', title: '', author: '', read: false };

  constructor(private bookService: BookService) {}

  ngOnInit() {
    this.loadBooks();
  }

  loadBooks() {
    this.bookService.getBooks().subscribe(data => {
      this.books = data;
      this.isEditing = new Array(this.books.length).fill(false);
    });
  }

  addBook() {
    this.addingNewBook = true;
    this.newBook = { id: '', title: '', author: '', read: false };
  }

  saveNewBook() {
    this.bookService.createBook(this.newBook).subscribe(() => {
      this.addingNewBook = false;
      this.loadBooks(); 
    });
  }

  editBook(index: number) {
    this.isEditing[index] = true;
  }

  saveBook(index: number) {
    const book = this.books[index];
    this.bookService.updateBook(String(book.id), book).subscribe(() => {
      this.isEditing[index] = false;
      this.loadBooks();
    });
  }

  confirmDelete(book: Book) {
    this.showModal = true;
    this.deleteId = String(book.id);
  }

  deleteBook() {
    if (this.deleteId !== null) {
      this.bookService.deleteBook(String(this.deleteId)).subscribe(() => {
        this.loadBooks();
        this.closeModal(); 
      });
    }
  }

  closeModal() {
    this.showModal = false;
    this.deleteId = null;
  }

  isSaveDisabled(): boolean {
    return !this.newBook.title.trim() || !this.newBook.author.trim();
  }
}