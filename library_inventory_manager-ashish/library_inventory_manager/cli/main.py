"""Command-line interface for the Library Inventory Manager."""
import logging, sys
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

LOG_FILE = 'data/app.log'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
                    handlers=[logging.FileHandler(LOG_FILE, encoding='utf-8'),
                              logging.StreamHandler(sys.stdout)])

logger = logging.getLogger('library_cli')

def input_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print('Input cannot be empty. Please try again.')

def menu():
    inv = LibraryInventory()
    while True:
        print('\n=== Library Inventory Manager ===')
        print('1. Add Book')
        print('2. Issue Book')
        print('3. Return Book')
        print('4. View All Books')
        print('5. Search by Title')
        print('6. Search by ISBN')
        print('7. Exit')
        choice = input('Choose an option (1-7): ').strip()
        try:
            if choice == '1':
                title = input_nonempty('Title: ')
                author = input_nonempty('Author: ')
                isbn = input_nonempty('ISBN: ')
                try:
                    inv.add_book(Book(title=title, author=author, isbn=isbn))
                    print('Book added successfully.')
                except ValueError as ve:
                    print('Error:', ve)
            elif choice == '2':
                isbn = input_nonempty('ISBN to issue: ')
                try:
                    inv.issue_book(isbn)
                    print('Book issued.')
                except Exception as e:
                    print('Error:', e)
            elif choice == '3':
                isbn = input_nonempty('ISBN to return: ')
                try:
                    inv.return_book(isbn)
                    print('Book returned.')
                except Exception as e:
                    print('Error:', e)
            elif choice == '4':
                books = inv.display_all()
                if not books:
                    print('No books in catalog.')
                for b in books:
                    print('-', b)
            elif choice == '5':
                t = input_nonempty('Title search keyword: ')
                results = inv.search_by_title(t)
                if not results:
                    print('No matches.')
                for b in results:
                    print('-', b)
            elif choice == '6':
                isbn = input_nonempty('ISBN to search: ')
                b = inv.search_by_isbn(isbn)
                if not b:
                    print('Not found.')
                else:
                    print(b)
            elif choice == '7':
                print('Goodbye!')
                break
            else:
                print('Invalid choice, choose 1-7.')
        except KeyboardInterrupt:
            print('\nInterrupted. Exiting.')
            break
        except Exception as e:
            logger.error('An error occurred in menu loop', exc_info=True)
            print('An unexpected error occurred:', e)

if __name__ == '__main__':
    menu()
