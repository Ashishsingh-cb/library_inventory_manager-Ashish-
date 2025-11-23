"""Book class for the Library Inventory Manager."""
from dataclasses import dataclass, asdict

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # 'available' or 'issued'

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self):
        return asdict(self)

    def issue(self):
        if self.status == "issued":
            raise ValueError("Book already issued.")
        self.status = "issued"

    def return_book(self):
        if self.status == "available":
            raise ValueError("Book is already marked available.")
        self.status = "available"

    def is_available(self):
        return self.status == "available"
