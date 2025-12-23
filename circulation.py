from datetime import datetime, timedelta

def checkout_book(books: list, patrons: list, loans: list, isbn: str, library_id: str, loan_period_days: int) -> dict:

    book = next((b for b in books if b["isbn"] == isbn), None)
    patron = next((p for p in patrons if p["library_id"] == library_id), None)

    if not book or not patron:
        return {"Error": "Book or patron not found"}

    patron_loans = [l for l in loans if l["library_id"] == library_id]
    if len(patron_loans) >= patron.get("borrowing_limit", 5):
        return {"Error": "Patron reached the borrowing limit."}

    if book.get("copies_available", 0) <= 0:
        return {"Error": "No copies available."}
    
    due_date = (datetime.now() + timedelta(days=loan_period_days)).strftime("%Y-%m-%d")
    history_count = len(patron.get("borrowing_history", []))
    loan_id = f"L{len(loans) + history_count + 1000}"
    new_loan = {
        "loan_id": loan_id,
        "isbn": isbn, 
        "library_id": library_id, 
        "due_date": due_date
    }
    loans.append(new_loan)
    book["copies_available"] -= 1
    return new_loan


def return_book(books: list, patrons: list, loans: list, loan_id: str, return_date: str) -> dict: 
    loan = next((l for l in loans if l["loan_id"] == loan_id), None)
    if not loan:
        return {"Error": "Loan not found"}

    book = next((b for b in books if b["isbn"] == loan["isbn"]), None)
    if book:
        book["copies_available"] += 1

    try:    
        due = datetime.strptime(loan["due_date"], "%Y-%m-%d")
        returned = datetime.strptime(return_date, "%Y-%m-%d")
        overdue_days = max((returned - due).days, 0)
    except ValueError:
        return {"Error": "Invalid date format."}
    
    if overdue_days > 0:
        apply_fine(patrons, loan["library_id"], overdue_days * 1.0)

    patron = next((p for p in patrons if p["library_id"] == loan["library_id"]), None)
    if patron:
        closed_loan = loan.copy()
        closed_loan["return_date"] = return_date
        if "borrowing_history" not in patron:
            patron["borrowing_history"] = []
        patron["borrowing_history"].append(closed_loan)

    loans.remove(loan)
    return {"status": "returned", "overdue_days": overdue_days}


def renew_loan(loans: list, loan_id: str, extension_days: int) -> dict:
    loan = next((l for l in loans if l["loan_id"] == loan_id), None)
    if not loan:
        return {"Error": "Loan not found."}
    try:
        due_date = datetime.strptime(loan["due_date"], "%Y-%m-%d")
        new_due_date = due_date + timedelta(days=extension_days)
        loan["due_date"] = (due_date + timedelta(days=extension_days)).strftime("%Y-%m-%d")
        return loan
    except:
        return {"Error": "Date error during renewal."}


def apply_fine(patrons: list, library_id: str, amount: float) -> dict:
    for p in patrons:
        if p.get("library_id") == library_id:
            current_fines = p.get("fines", 0.0)
            p["fines"] += amount
            return p
    return None


def list_patron_loans(loans: list, library_id: str) -> list:
    results = []
    for loan in loans:
        if loan.get("library_id") == library_id:
            results.append(loan)
    return results












