import unittest
from datetime import datetime, timedelta
import catalog
import circulation
import patron

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.books = [
            {
                "isbn": "111", 
                "title": "Test Book 1", 
                "authors": ["Author A"], 
                "year": 2020, 
                "genre": "Fiction", 
                "copies_owned": 2, 
                "copies_available": 2, 
                "retired": False
            },
            {
                "isbn": "222", 
                "title": "Test Book 2", 
                "authors": ["Author B"], 
                "year": 2021, 
                "genre": "Romance", 
                "copies_owned": 1, 
                "copies_available": 1, 
                "retired": False
            }
        ]
        self.patrons = [
            {
                "library_id": "P1", 
                "name": "Test Patron", 
                "borrowing_limit": 2, 
                "borrowing_history": [], 
                "fines": 0.0
            }
        ]
        self.loans = []

    def test_due_date_calculation(self):
        loan_period = 14
        result = circulation.checkout_book(self.books, self.patrons, self.loans, "111", "P1", loan_period)
        
        expected_date = (datetime.now() + timedelta(days=loan_period)).strftime("%Y-%m-%d")
        
        self.assertEqual(result['due_date'], expected_date)

    def test_search_functionality(self):
        results = catalog.filter_books(self.books, genre="Romance")
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], "Test Book 2")

    def test_borrowing_limit(self):
        circulation.checkout_book(self.books, self.patrons, self.loans, "111", "P1", 14)
        circulation.checkout_book(self.books, self.patrons, self.loans, "222", "P1", 14)
        
        self.books.append({"isbn": "333", "title": "Extra Book", "copies_available": 1})
        
        result = circulation.checkout_book(self.books, self.patrons, self.loans, "333", "P1", 14)

        self.assertTrue("Error" in result)

if __name__ == '__main__':
    unittest.main()