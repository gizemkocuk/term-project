import json

def load_patrons(path: str) -> list:
        try:
            with open(path, "r", encoding="utf-8") as fh:
                patrons_list = json.load(fh)
                return patrons_list
        except FileNotFoundError:
            return []
        except Exception:
            print(f"Error loading patrons: {e}")
            return []


def save_patrons(path: str, patrons: list) -> None:
    try:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(patrons, fh, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving patrons: {e}")


def register_patron(patrons: list, patron_data: dict) -> dict:
    patron_id = patron_data.get("library_id")
    if not patron_id:
        print("Error: Library ID is required.")
        return None
    for p in patrons:
        if p["library_id"] == patron_id:
            print("A patron with this ID is already exists.")
            return None
    try:
        new_patron = {
            "name": patron_data.get("name", "Unknown"),
            "email": patron_data.get("email", "Unknown"),
            "library_id": patron_data.get("library_id"),
            "contact_info": patron_data.get("contact_info", {}), 
            "borrowing_limit": 5,
            "password": patron_data.get("password", "1234"),
            "fines": 0.0,
            "borrowing_history": []
        }
        patrons.append(new_patron)
        return new_patron
    except Exception as e:
        print(f"Error registering patron: {e}")
        return None


def authenticate_patron(patrons: list, library_id: str, password: str) -> dict | None:
    for p in patrons:
        if p.get("library_id") == library_id and p.get("password") == password:
            return p
    print("Invalid ID or password")
    return None


def update_patron_contact(patrons: list, library_id: str, contact_updates: dict) -> dict:
    for patron in patrons:
        if patron.get("library_id") == library_id:
            try:
                for key, value in contact_updates.items():
                    if key not in ["library_id", "fines", "borrowing_history", "borrowing_limit"]:
                        patron[key] = value
                return patron
            except Exception as e:
                print(f"Error updating contact: {e}")
                return None
    print("Error: Patron not found.")
    return None