# Library Management System

A terminal-driven library system that maintains book inventory, borrower accounts, and circulation history.

## Setup

* **Prerequisites:** Python 3.x must be installed on your system.
* **Data:** The project includes a `data/` folder containing the necessary runtime files (`books.json`, `patrons.json`, `loans.json`).
* **How to Run:**
    Open your terminal in the project directory and run the command:

    python main.py

## Roles

### 1. Librarian (Administrator)
* **Role:** Access to manage books, register patrons, process loans, and view reports.
* **Password:** `admin` (Select Option 1 in the main menu).

### 2. Patron (Library User)
* **Role:** View personal loan history, search for books, and renew items.
* **Sample User:**
    * **Library ID:** `P001`
    * **Password:** `1234`
* **Note:** All other sample users found in `patrons.json` use the same password (`1234`).

## Sample Workflows

You can follow these scenarios to test the system functionalities:

**Scenario 1: Checking Out a Book (Librarian)**
1.  Run the program and select **1. Librarian Login** (Password: `admin`).
2.  Select **5. Checkout Book**.
3.  Enter ISBN: `978-1557427663` (*The Metamorphosis*).
4.  Enter Patron ID: `P001`.
5.  The system will confirm the loan and display the due date.

**Scenario 2: Patron Self-Service**
1.  Run the program and select **2. Patron Login**.
2.  Enter ID: `P001` and Password: `1234`.
3.  Select **1. Search Books** to find available titles (e.g., type "Classic").
4.  Select **2. My Loans & Returns** to see the book borrowed in Scenario 1.
5.  Select **3. Renew Loan** to extend the due date.

**Scenario 3: System Maintenance & Analytics (Librarian)**
1.  Log in as Librarian (`admin`).
2.  Select **2. Update Book Details** to change stock counts for an ISBN.
3.  Select **3. Retire Book** to remove a book from active circulation.
4.  Select **7. Reports & Analytics** and choose **3. Circulation Stats** to see the "Most Active Patron".
5.  Select **8. Backup System** to save a timestamped copy of all data to the `backups/` folder.
