import json
from datetime import datetime

def load_books(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            books_list = json.load(fh)
            return books_list
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error: {e}") 
        return []


def save_books(path: str, books: list) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(books, fh, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error: Failed to save changes. {e}")


def add_book(books: list, book_data: dict) -> dict: 
    isbn = book_data.get("isbn")
    if not isbn:
        print("Error: isbn is required to add a book.")
        return None
    for book in books:
        if book.get("isbn") == isbn:
            print(f"Error: A book with isbn {isbn} already exists.")
            return None
    try:
        copies = int(book_data.get("copies_owned", 1))
        if copies <= 0:         
            print("The number of owned copies must be at least 1.")
            return None
        year_raw = book_data.get("year")
        if year_raw is None:
            year_val = None
        else:
            try:
                year_val = int(year_raw)
            except ValueError:
                print("Error: Year must be a valid number.")
                return None
        new_book = {
            "isbn": isbn,
            "title": book_data.get("title", "unknown"),
            "authors": book_data.get("authors", ["unknown"]),
            "year": year_val,
            "genre": book_data.get("genre", "unknown"),
            "copies_owned": copies,
            "copies_available": copies,
            "retired": False,
            "added_date": datetime.now().strftime("%Y-%m-%d")
        }
        books.append(new_book)
        return new_book
    except Exception as e:
        print(f"Error: {e}")
        return None



def update_book(books: list, isbn: str, updates: dict) -> dict:
    for book in books:
        if book.get("isbn") == isbn:
            try:
                if "copies_owned" in updates:
                    new_owned = int(updates["copies_owned"])
                    if new_owned < 0:
                        print("The number of owned copies cannot be negative.")
                        return None
                    copies_loaned = book["copies_owned"] - book["copies_available"]
                    if new_owned < copies_loaned:
                        print("The number of loaned books cannot be more than the number of owned books.")
                        return None
                    book["copies_owned"] = new_owned
                    book["copies_available"] = new_owned - copies_loaned
                for key, value in updates.items():
                    if key in book and key not in ("isbn", "copies_available"):
                        book[key] = value
                return book
            except Exception as e:
                print(f"Error: {e}")
                return None
    return None


def soft_delete(books: list, isbn: str) -> bool:
    for book in books:
        if book.get("isbn") == isbn:
            book["retired"] = True
            return True
    return False


def search_books(books: list, keyword: str) -> list:
    if not keyword:
        return books
    keyword = keyword.lower().strip()
    results = []
    for book in books:
        if book.get("retired"): 
            continue
        title = book.get("title", "").lower()
        authors = " ".join(book.get("authors", [])).lower()
        if keyword in title or keyword in authors:
            results.append(book)
    return results


def filter_books(books: list, *, genre: str | None = None, year: int | None = None) -> list:
    results = [b for b in books if not b.get("retired")]
    if genre:
        genre_lower = genre.lower().strip()
        filtered_by_genre = []
        for book in results:
            book_genre = book.get("genre", "").lower()
            if book_genre == genre_lower:
                filtered_by_genre.append(book)
        results = filtered_by_genre
    if year is not None:
        filtered_by_year = []
        try:
            year_int = int(year)
        except ValueError:
            print("Year must be a number.")
            return []
        for book in results:
            book_year = book.get("year")
            if book_year == year_int:
                filtered_by_year.append(book)
        results = filtered_by_year
    return results


def new_arrivals(books: list, limit: int = 5) -> list:
    active_books = [b for b in books if not b.get("retired")]
    sorted_books = sorted(active_books, key=lambda b: b.get("added_date", ""), reverse=True)
    return sorted_books[:limit]

