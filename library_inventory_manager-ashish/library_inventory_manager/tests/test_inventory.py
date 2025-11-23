import os, tempfile
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

def test_add_and_search():
    # use temp files to avoid clashing with real data
    tmp_csv = 'data/test_catalog.csv'
    tmp_txt = 'data/test_catalog.txt'
    inv = LibraryInventory(csv_path=tmp_csv, txt_path=tmp_txt)
    # ensure clean start
    if os.path.exists(tmp_csv):
        os.remove(tmp_csv)
    if os.path.exists(tmp_txt):
        os.remove(tmp_txt)
    inv = LibraryInventory(csv_path=tmp_csv, txt_path=tmp_txt)
    b = Book(title='Test Driven', author='Tester', isbn='1111')
    inv.add_book(b)
    assert inv.search_by_isbn('1111') is not None
    # cleanup
    if os.path.exists(tmp_csv):
        os.remove(tmp_csv)
    if os.path.exists(tmp_txt):
        os.remove(tmp_txt)
