
def checkout_book(books: list, patrons: list, loans: list, isbn: str, library_id: str, loan_period_days: int) -> dict:


def return_book(books: list, patrons: list, loans: list, loan_id: str, return_date: str) -> dict: 


def renew_loan(loans: list, loan_id: str, extension_days: int) -> dict: 


def apply_fine(patrons: list, library_id: str, amount: float, overdue_days: int, daily_rate: float) -> dict: 
    for p in patrons:
        if p.get("library_id") == library_id:
            fine_amount = overdue_days * daily_rate
            p["fines"] += fine_amount
            return p
    return None


def list_patron_loans(loans: list, library_id: str) -> list:
    result = []
    for loan in loans:
        if loan.get("library_id") == library_id:
            result.append(loan)
    return result


#Borrowing checks availability, enforces per-patron limits, and sets due dates.
#Returning updates availability, calculates fines, and records completion.
#Support renewals if no active holds exist.
#Optional: hold/reservation queue.









