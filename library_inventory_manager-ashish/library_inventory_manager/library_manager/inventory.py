"""Inventory management: load/save from CSV/TXT and basic operations."""
import csv, logging, os
from library_manager.book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self, csv_path='data/catalog.csv', txt_path='data/catalog.txt'):
        self.csv_path = csv_path
        self.txt_path = txt_path
        self.books = []
        # ensure data dir exists
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self.load_from_csv()

    def add_book(self, book: Book):
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError(f"ISBN {book.isbn} already exists in inventory.")
        self.books.append(book)
        self.save_to_csv()
        logger.info(f"Added book: {book}")

    def search_by_title(self, title):
        return [b for b in self.books if title.lower() in b.title.lower()]

    def search_by_isbn(self, isbn):
        return next((b for b in self.books if b.isbn == isbn), None)

    def display_all(self):
        return list(self.books)

    def issue_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise LookupError("Book not found.")
        book.issue()
        self.save_to_csv()
        logger.info(f"Issued book: {book}")

    def return_book(self, isbn):
        book = self.search_by_isbn(isbn)
        if not book:
            raise LookupError("Book not found.")
        book.return_book()
        self.save_to_csv()
        logger.info(f"Returned book: {book}")

    def save_to_csv(self):
        try:
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['title','author','isbn','status'])
                for b in self.books:
                    writer.writerow([b.title, b.author, b.isbn, b.status])
            # also save a human-readable txt
            with open(self.txt_path, 'w', encoding='utf-8') as f:
                for b in self.books:
                    f.write(str(b) + '\n')
        except Exception as e:
            logger.error(f"Failed to save catalog: {e}")
            raise

    def load_from_csv(self):
        self.books = []
        if not os.path.exists(self.csv_path):
            # create an empty file
            try:
                open(self.csv_path, 'w', encoding='utf-8').close()
                open(self.txt_path, 'w', encoding='utf-8').close()
            except Exception as e:
                logger.error(f"Could not create data files: {e}")
            return
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if not row.get('isbn'):
                        continue
                    # basic validation
                    title = row.get('title','').strip()
                    author = row.get('author','').strip()
                    isbn = row.get('isbn','').strip()
                    status = row.get('status','available').strip().lower()
                    if status not in ('available','issued'):
                        status = 'available'
                    self.books.append(Book(title=title, author=author, isbn=isbn, status=status))
        except Exception as e:
            logger.error(f"Failed to load catalog (may be corrupted): {e}")
            # attempt to recover by truncating file
            try:
                open(self.csv_path, 'w', encoding='utf-8').close()
            except Exception:
                pass
