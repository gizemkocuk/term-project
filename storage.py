import json

def ensure_data_paths(base_dir: str) -> None:
    filenames = ["books.json", "patrons.json", "loans.json"]
    for filename in filenames:
        path = f"{base_dir}/{filename}"
        try:
            with open(path, "r", encoding="utf-8"):
                pass
        except FileNotFoundError:
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)


def load_state(base_dir: str) -> tuple[list, list, list]:
    books, patrons, loans = [], [], []
    try:
        with open(f"{base_dir}/books.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        books = []
    try:
        with open(f"{base_dir}/patrons.json", "r", encoding="utf-8") as f:
            patrons = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        patrons = []
    try:
        with open(f"{base_dir}/loans.json", "r", encoding="utf-8") as f:
            loans = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        loans = []
    return books, patrons, loans


def save_state(base_dir: str, books: list, patrons: list, loans: list) -> None:
    try:
        with open(f"{base_dir}/books.json", "w", encoding="utf-8") as f:
            json.dump(books, f, indent=4, ensure_ascii=False)
        with open(f"{base_dir}/patrons.json", "w", encoding="utf-8") as f:
            json.dump(patrons, f, indent=4, ensure_ascii=False)
        with open(f"{base_dir}/loans.json", "w", encoding="utf-8") as f:
            json.dump(loans, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"error: {e}")


import shutil#
from datetime import datetime

def backup_state(base_dir: str, backup_dir: str) -> list[str]:
    backup_files = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filenames = ["books.json", "patrons.json", "loans.json"]
    for filename in filenames:
        src = f"{base_dir}/{filename}"
        dst = f"{backup_dir}/{timestamp}_{filename}"
        try:
            shutil.copy(src, dst)
            backup_files.append(dst)
        except FileNotFoundError:
            continue
    return backup_files


def validate_catalog_schema(books: list) -> bool:
    required_fields = {
        "isbn", "title", "authors", "year", "genre", 
        "copies_owned", "copies_available", "retired", "added_date"
    }
    for book in books:
        if not required_fields.issubset(book.keys()):#
            return False
        if not isinstance(book["isbn"], str) or len(book["isbn"].strip()) == 0:
            return False
        if not isinstance(book["title"], str) or len(book["title"].strip()) == 0:
            return False
        if not (isinstance(book["authors"], list) or isinstance(book["authors"], str)):
            return False
        if not isinstance(book["year"], int):
            return False
        if not isinstance(book["genre"], str) or len(book["genre"].strip()) == 0:
            return False
        if not isinstance(book["copies_owned"], int) or not isinstance(book["copies_available"], int):
            return False
        if book["copies_available"] > book["copies_owned"]:
            return False
        if not isinstance(book["retired"], bool):
            return False
        if not isinstance(book["added_date"], str):
            return False
    return True