from datetime import datetime
import csv
import json

def overdue_report(loans: list, current_date: str) -> list:
    overdue_items = []
    date_format = "%Y-%m-%d"
    try:
        current_dt = datetime.strptime(current_date, date_format)
    except ValueError:
        return []
    for loan in loans:
        if loan.get('return_date') is not None:
            continue
        due_date_str = loan.get('due_date')
        if not due_date_str:
            continue  
        try:
            due_dt = datetime.strptime(due_date_str, date_format)
            if current_dt > due_dt:
                overdue_days = (current_dt - due_dt).days
                overdue_info = {
                    "loan_id": loan.get("loan_id"),
                    "isbn": loan.get("isbn"),
                    "library_id": loan.get("library_id"),
                    "due_date": due_date_str,
                    "days_overdue": overdue_days
                }
                overdue_items.append(overdue_info)     
        except ValueError:
            continue
    return overdue_items


def fines_summary(patrons: list) -> dict:
    summary = {
        "total_outstanding_fines": 0.0,
        "patrons_with_fines": []
    }
    for patron in patrons:
        amount = patron.get("fines", 0.0)
        if amount > 0:
            summary["total_outstanding_fines"] += amount
            summary["patrons_with_fines"].append({
                "library_id": patron.get("library_id"),
                "name": patron.get("name"),
                "amount": round(amount, 2)
            })
    summary["total_outstanding_fines"] = round(summary["total_outstanding_fines"], 2)
    return summary


def circulation_stats(loans: list, books: list) -> dict:
    stats = {
        "total_loans": len(loans),
        "loans_per_genre": {},
        "most_borrowed_book": None,
        "most_active_patron": None
    }
    book_loan_counts = {}
    patron_loan_counts = {}

    books_map = {b["isbn"]: b for b in books}

    for loan in loans:
        isbn = loan.get("isbn")
        if isbn:
            book_loan_counts[isbn] = book_loan_counts.get(isbn, 0) + 1
            if isbn in books_map:
                genre = books_map[isbn].get("genre", "Unknown")
                stats["loans_per_genre"][genre] = stats["loans_per_genre"].get(genre, 0) + 1
        patron_id = loan.get('library_id')
        if patron_id:
            patron_loan_counts[patron_id] = patron_loan_counts.get(patron_id, 0) + 1

    if book_loan_counts:
        most_popular_isbn = max(book_loan_counts, key=book_loan_counts.get)
        count = book_loan_counts[most_popular_isbn]
        title = books_map.get(most_popular_isbn, {}).get("title", "Unknown Title")
        stats["most_borrowed_book"] = {
            "isbn": most_popular_isbn,
            "title": title,
            "count": count
        }
    if patron_loan_counts:
        most_active_id = max(patron_loan_counts, key=patron_loan_counts.get)
        count = patron_loan_counts[most_active_id]
        stats["most_active_patron"] = {
            "library_id": most_active_id,
            "count": count
        }
    return stats


def export_report(report: dict | list, filename: str) -> str:
    try:
        if isinstance(report, list) and len(report) > 0:
            if not filename.endswith('.csv'):
                filename += '.csv'
            keys = report[0].keys()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(report)
        elif isinstance(report, dict):
            if not filename.endswith('.txt'):
                filename += '.txt'
            with open(filename, 'w', encoding='utf-8') as f:
                for key, value in report.items():
                    if isinstance(value, (dict, list)):
                        f.write(f"{key}:\n")
                        f.write(json.dumps(value, indent=4, ensure_ascii=False))
                        f.write("\n" + "-"*20 + "\n")
                    else:
                        f.write(f"{key}: {value}\n")
        else:
            return "Error: Empty or invalid report format."
        return filename
    except Exception as e:
        return f"Error: {str(e)}"


