#data/books.json
import json
books = [
    {
    "isbn": "978-1557427663",
    "title": "The Metamorphosis",
    "authors": ["Franz Kafka"],
    "year": 1915,
    "genre": "Novella",
    "copies_owned": 2,
    "copies_available": 2
    },
    {
    "isbn": "978-9176052242",
    "title": "Anna Karenina",
    "authors": ["Leo Tolstoy"],
    "year": 1878,
    "genre": "Realist Fiction",
    "copies_owned": 5,
    "copies_available": 4
    },
    {
    "isbn": "978-0141439518",
    "title": "Pride and Prejudice",
    "authors": ["Jane Austen"],
    "year": 1813,
    "genre": "Romance",
    "copies_owned": 4,
    "copies_available": 4
    },
    {
    "isbn": "978-0060853983",
    "title": "Good Omens",
    "authors": ["Neil Gaiman", "Terry Pratchett"],
    "year": 1990,
    "genre": "Fantasy",
    "copies_owned": 3,
    "copies_available": 3
    }
]

with open("books.json", "w", encoding="utf-8") as fh: 
    json.dump(books, fh, indent=2, ensure_ascii=False) 


def load_books(path: str) -> list:
   try:
    with open(path, "r", encoding="utf-8") as fh:
        books_list = json.load(fh)
        return books_list
#except:




def save_books(path: str, books: list) -> None: ... 
def add_book(books: list, book_data: dict) -> dict: ... 
def update_book(books: list, isbn: str, updates: dict) -> dict: ... 
def search_books(books: list, keyword: str) -> list: ... 
def filter_books(books: list, *, genre: str | None = None, year: int | 
None = None) -> list: ... 
