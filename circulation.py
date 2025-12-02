
from datetime import datetime, timedelta

def checkout_book(books: list, patrons: list, loans: list, isbn: str, library_id: str, loan_period_days: int) -> dict:

    book = next((b for b in books if b["isbn"] == isbn), None)#
    patron = next((p for p in patrons if p["library_id"] == library_id), None)
    
    if not book or not patron:
        return {"error" : "Book or patron not found"}

    patron_loans = [l for l in loans if l["library_id"] == library_id]
    if len(patron_loans) >= patron.get("borrowing_limit", 5):
        return {"error:" "Patron reached the borrowing limit."}
    
    if book["available"] <= 0:
        return {"error:" "No copies available"}
 
    due_date = (datetime.now() + timedelta(days=loan_period_days)).strftime("%Y-%m-%d")#
    loan_id = f"L{len(loans)+1}"
    new_loan = {"loan_id": loan_id, "isbn": isbn, "library_id": library_id, "due_date": due_date}
    loans.append(new_loan)

    book["available"] -= 1
    
    return new_loan



def return_book(books: list, patrons: list, loans: list, loan_id: str, return_date: str) -> dict: 
    
    loan = next((l for l in loans if l["loan_id"] == loan_id), None)
    if not loan:
        return {"error:" "Loan not found"}

    book = next((b for b in books if b["isbn"] == loan["isbn"]), None)
    if book:
        book["available"] += 1
    
    due = datetime.strptime(loan["due_date"], "%Y-%m-%d")
    returned = datetime.strptime(return_date, "%Y-%m-%d")
    overdue_days = max((returned - due).days, 0)
    
    if overdue_days > 0:
        apply_fine(patrons, loan["library_id"], 0, overdue_days, 1)
    loans.remove(loan)
    
    return {"status": "returned", "overdue_days": overdue_days}#



def renew_loan(loans: list, loan_id: str, extension_days: int) -> dict:
    
    loan = next((l for l in loans if l["loan_id"] == loan_id), None)
    if not loan:
        return {"error" "Loan not found"}
    
    due_date = datetime.strptime(loan["due_date"], "%Y-%m-%d")
    loan["due_date"] = (due_date + timedelta(days=extension_days)).strftime("%Y-%m-%d")
    
    return loan
#Support renewals if no active holds exist.


def apply_fine(patrons: list, library_id: str, amount: float, overdue_days: int, daily_rate: float) -> dict: 
    
    for p in patrons:
        if p.get("library_id") == library_id:
            fine_amount = overdue_days * daily_rate
            p["fines"] += fine_amount
            return p
    return None


def list_patron_loans(loans: list, library_id: str) -> list:
    
    results = []
    for loan in loans:
        if loan.get("library_id") == library_id:
            results.append(loan)
    return results


#Optional: hold/reservation queue.









