import sys
import os
from datetime import datetime

import catalog
import patron
import circulation
import storage
import reports

DATA_DIR = "data"
BACKUP_DIR = "backups"
LOAN_PERIOD_DAYS = 14

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    print("\n" + "=" * 40)
    print(f" {title.upper()}")
    print("=" * 40)


def librarian_menu(books, patrons, loans):
    while True:
        print_header("Librarian Panel")
        print("1. Add New Book")
        print("2. Update Book Details")
        print("3. Retire Book")
        print("4. Register New Patron")
        print("5. Checkout Book")
        print("6. Return Book")
        print("7. Reports & Analytics")
        print("8. Backup System")
        print("0. Return to Main Menu")
        
        choice = input("\nSelect an option: ")

        if choice == '1':
            print_header("Add Book")
            isbn = input("ISBN: ")
            title = input("Title: ")
            authors = input("Authors (comma separated): ").split(',')
            authors = [a.strip() for a in authors]
            year = input("Year: ")
            genre = input("Genre: ")
            copies = input("Copies: ")
            
            book_data = {
                "isbn": isbn, 
                "title": title, 
                "authors": authors,
                "year": int(year) if year.isdigit() else 2000,
                "genre": genre, 
                "copies_owned": int(copies) if copies.isdigit() else 1
            }
            result = catalog.add_book(books, book_data)
            if result: 
                print("Book added successfully.")

        elif choice == '2':
            isbn = input("ISBN to update: ")
            print("Fields: title, genre, copies_owned")
            field = input("Field to update: ")
            value = input("New value: ")
            updates = {field: value}
            result = catalog.update_book(books, isbn, updates)
            if result: print("Book updated successfully.")
            else: print("Update failed.")

        elif choice == '3':
            isbn = input("ISBN to retire: ")
            confirm = input(f"{isbn} will be retired. Are you sure? (y/n): ")
            if confirm.lower() == 'y':
                if catalog.soft_delete(books, isbn):
                    print("Book retired successfully.")
                else:
                    print("Error: Book not found.")

        elif choice == '4':
            print_header("Register Patron")
            p_data = {
                "library_id": input("Library ID: "),
                "name": input("Full Name: "),
                "email": input("Email: "),
                "password": input("Password: ")
            }
            res = patron.register_patron(patrons, p_data)
            if res: print(f"Patron {res['name']} registered.")

        elif choice == '5':
            print_header("Checkout Book")
            isbn = input("ISBN: ")
            lib_id = input("Patron ID: ")
            result = circulation.checkout_book(books, patrons, loans, isbn, lib_id, LOAN_PERIOD_DAYS)
            if result and "Error" in result:
                print(f"Error: {result['Error']}")
            elif result:
                print(f"Checkout successful. Due Date: {result.get('due_date')}")

        elif choice == '6':
            print_header("Return Book")
            loan_id = input("Loan ID: ")
            today = datetime.now().strftime("%Y-%m-%d")
            result = circulation.return_book(books, patrons, loans, loan_id, today)
            
            if result and "Error" in result:
                print(f"Error: {result.get('Error')}")
            else:
                print("Book returned successfully.")
                if result.get("overdue_days", 0) > 0:
                    days = result['overdue_days']
                    print(f"This book is {days} days overdue.")

        elif choice == '7':
            reporting_menu(books, patrons, loans)

        elif choice == '8':
            if not os.path.exists(BACKUP_DIR):
                os.makedirs(BACKUP_DIR)
            files = storage.backup_state(DATA_DIR, BACKUP_DIR)
            print(f"Backup created.")

        elif choice == '0':
            break
        else:
            print("Invalid selection.")


def reporting_menu(books, patrons, loans):
    while True:
        print_header("Reports")
        print("1. Overdue List")
        print("2. Fines Summary")
        print("3. Circulation Stats")
        print("4. Export Report")
        print("0. Back")
        
        c = input("Selection: ")
        if c == '1':
            today = datetime.now().strftime("%Y-%m-%d")
            overdues = reports.overdue_report(loans, today)
            if not overdues:
                print("No overdue books found.")
            for item in overdues:
                print(f"Loan: {item['loan_id']}| Overdue: {item['days_overdue']} days")
        
        elif c == '2':
            summary = reports.fines_summary(patrons)
            print(f"Total Outstanding Fines: {summary['total_outstanding_fines']}")
            for p in summary['patrons_with_fines']:
                print(f"- {p['name']}: {p['amount']}")

        elif c == '3':
            stats = reports.circulation_stats(loans, books)
            print(f"Total Active Loans: {stats['total_loans']}")
            if stats['most_borrowed_book']:
                b = stats['most_borrowed_book']
                print(f"Most Popular Book: {b['title']} (Borrowed {b['count']} times)")
            if stats['most_active_patron']:
                p = stats['most_active_patron']
                print(f"Most Active Patron ID: {p['library_id']} (Borrowed {p['count']} times)")
        elif c == '4':
            print("\n--- Export Menu ---")
            print("1. Export Overdue Report")
            print("2. Export Fines Summary")
            sub_c = input("Choose report: ")
            filename = input("Filename: ")
            msg = ""
            if sub_c == '1':
                today = datetime.now().strftime("%Y-%m-%d")
                data = reports.overdue_report(loans, today)
                msg = reports.export_report(data, filename)
            elif sub_c == '2':
                data = reports.fines_summary(patrons)
                msg = reports.export_report(data, filename)
            print(f"Export result: {msg}")

        elif c == '0':
            break


def patron_menu(books, patrons, loans, current_patron):
    while True:
        print_header(f"Welcome, {current_patron['name']}")
        print("1. Search Books")
        print("2. My Loans & Returns")
        print("3. Renew Loan")
        print("4. Update Contact Info")
        print("0. Logout")

        choice = input("\nSelect an option: ")

        if choice == '1':
            key = input("Search keyword: ")
            results = catalog.search_books(books, key)
            print(f"\n{len(results)} books found:")
            for b in results:
                status = "Available" if b['copies_available'] > 0 else "Out of Stock"
                print(f"- {b['title']} ({b['authors'][0]}) [{status}] ISBN: {b['isbn']}")

        elif choice == '2':
            my_loans = circulation.list_patron_loans(loans, current_patron['library_id'])
            if not my_loans:
                print("No active loans.")
            for l in my_loans:
                print(f"LoanID: {l['loan_id']} | ISBN: {l['isbn']} | Due: {l['due_date']}")

        elif choice == '3':
            lid = input("Loan ID to renew: ")
            res = circulation.renew_loan(loans, lid, 7)
            if res and "Error" in res:
                print("Error: Could not renew loan.")
            else:
                print(f"Renewed. New Due Date: {res['due_date']}")
        
        elif choice == '4':
            email = input("New Email: ")
            patron.update_patron_contact(patrons, current_patron['library_id'], {"email": email})
            print("Contact information updated.")

        elif choice == '0':
            break


def main():
    storage.ensure_data_paths(DATA_DIR)
    
    print("System initializing, loading data...")
    books, patrons, loans = storage.load_state(DATA_DIR)
    print(f"Data Loaded: {len(books)} Books, {len(patrons)} Patrons, {len(loans)} Loans.")

    while True:
        print_header("Library Management System")
        print("1. Librarian Login")
        print("2. Patron Login")
        print("3. Save & Exit")
        
        role = input("\nPlease select your role: ")

        if role == '1':
            pwd = input("Admin Password: ")
            if pwd == "admin":
                librarian_menu(books, patrons, loans)
            else:
                print("Invalid password.")

        elif role == '2':
            lib_id = input("Library ID: ")
            password = input("Password: ")
            user = patron.authenticate_patron(patrons, lib_id, password)
            if user:
                patron_menu(books, patrons, loans, user)
            else:
                print("Login failed. Invalid ID or password.")

        elif role == '3':
            print("Saving data...")
            storage.save_state(DATA_DIR, books, patrons, loans)
            print("Goodbye!")
            sys.exit()
        
        else:
            print("Invalid selection, please try again.")

if __name__ == "__main__":
    main()