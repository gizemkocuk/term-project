#data/patrons.json

import json

def load_patrons(path: str) -> list:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                patrons_list = json.load(fh)
                return patrons_list
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
        except Exception:
            return []

def save_patrons(path: str, patrons: list) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(patrons, fh, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"error:{e}")

#name, email, library ID#, contact info, and borrowing limits.
def register_patron(patrons: list, patron_data: dict) -> dict:
    patron_id = patron_data.get("library_id")
    if not patron_id:
        print("ID is required.")
        return None
    for p in patrons:
        if p["library_id"] == patron_id:
            print("A patron with this ID is already registered.")
            return None
    try:
        new_patron = {
            "name": patron_data.get("name", "unknown"),
            "email": patron_data.get("email", "unknown"),
            "library_id": patron_data.get("library_id"),
            "contact_info": patron_data.get("contact_info", "unknown"), 
            "borrowing_limit": 5,
            "password": patron_data.get("password", "1234")#
        }
        patrons.append(new_patron)
        return new_patron
    except Exception as e:
        print(f"error:{e}")
        return None

#Reject invalid ISBNs and duplicate library IDs.

def authenticate_patron(patrons: list, library_id: str, password: str) -> dict | None:
    for p in patrons:
        if p["library_id"] == library_id and p["password"] == password:
            return p
    print("Invalid ID or password") 
    return None


def update_patron_contact(patrons: list, library_id: str, contact_updates: 
dict) -> dict: