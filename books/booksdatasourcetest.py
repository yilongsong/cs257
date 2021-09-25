'''
Synopsis:

Tests use test.csv, containing 10 lines

Functions to test:
1) authors(self, search_text=None)
    Features to check:
        - search_text=None with correct tie breaking test
        - general test
        - case-insensitivity test
    (3 tests)
2) books(self, search_text=None, sort_by='title')
    Features to check:
        - search_text=None test
        - general test (combined with former)
        - case test
        - sort_by = 'year' test
    (4 tests)
3) books_between_years(self, start_year=None, end_year=None)
    Features to check:
        - None for both test
        - general test
        - start_year = None test
        - end_year = None test
    (5 tests)
'''


import booksdatasource
import unittest

class BooksDataSourceTester(unittest.TestCase):
    def setUp():
        self.books_data_source = booksdatasource.BooksDataSource(test.csv)
        
    def tearDown():
        pass
        
    #Tests for authors
    def test_authors_none(self):
        res = self.books_data_source.authors()
        authorGivennameList = ["Ann", "Charlotte", "Agatha", "Sinclair", "Tommy", "Laurence", "Connie"]
        authorSurnameList = ["Brontë", "Brontë", "Christie", "Lewis", "Orange", "Sterne", "Willis"]
        
        for i in range(len(res)):
            assertEqual(res[i].surname, authorSurnameList[i])
            assertEqual(res[i].given_name, authorGivennameList[i])
            
    def test_authors_general(self):
        res = self.books_data_source.authors("i")
        authorGivennameList = ["Agatha", "Sinclair", "Connie"]
        authorSurnameList = ["Christie", "Lewis", "Willis"]
        
        for i in range(len(res)):
            assertEqual(res[i].surname, authorSurnameList[i])
            assertEqual(res[i].given_name, authorGivennameList[i])
            
    def test_authors_case(self):
        res = self.books_data_source.authors("RON")
        authorGivennameList = ["Ann", "Charlotte"]
        authorSurnameList = ["Brontë", "Brontë"]
        
        for i in range(len(res)):
            assertEqual(res[i].surname, authorSurnameList[i])
            assertEqual(res[i].given_name, authorGivennameList[i])
            
    
    #Test for books
    def test_books_none(self):
        res1 = self.books_data_source.books()
        res2 = self.books_data_source.books(search_text=None, sort_by='abcd')
        bookTitleList = ["All Clear", "Blackout", "Elmer Gantry", "Jane Eyre", "Main Street", "Murder on the Orient Express","The Life and Opinions of Tristram Shandy, Gentleman", "The Tenant of Wildfell Hall", "There, There", "Villette"]
        
        for i in range(len(res)):
            assertEqual(res1[i].title, bookTitleList[i])
            assertEqual(res2[i].title, bookTitleList[i])
            
    def test_books_general(self):
        res = self.books_data_source.books(search_text = 'th')
        bookTitleList = ["The Life and Opinions of Tristram Shandy, Gentleman", "The Tenant of Wildfell Hall", "There, There"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
            
    def test_books_case(self):
        res = self.books_data_source.books(search_text = 'TH')
        bookTitleList = ["The Life and Opinions of Tristram Shandy, Gentleman", "The Tenant of Wildfell Hall", "There, There"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
        
    def test_books_year(self):
        res = self.books_data_source.books(search_text=None, sort_by='year')
        bookTitleList = ["The Life and Opinions of Tristram Shandy, Gentleman", "Jane Eyre", "The Tenant of Wildfell Hall", "Villette", "Main Street", "Elmer Gantry", "Murder on the Orient Express", "All Clear", "Blackout", "There, There"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
            
    #Test for books_between_years
    def test_books_between_years_both_none(self):
        res = self.books_data_source.books_between_years(start_year=None, end_year=None)
        bookTitleList = ["The Life and Opinions of Tristram Shandy, Gentleman", "Jane Eyre", "The Tenant of Wildfell Hall", "Villette", "Main Street", "Elmer Gantry", "Murder on the Orient Express", "All Clear", "Blackout", "There, There"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
    
    def test_books_between_years_general(self):
        res = self.books_data_source.books_between_years(start_year=1920, end_year = 1940)
        bookTitleList = ["Main Street", "Elmer Gantry", "Murder on the Orient Express"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
            
    def test_books_between_years_start_year_none(self):
        res = self.books_data_source.books_between_years(start_year=None, end_year=1900)
        bookTitleList = ["The Life and Opinions of Tristram Shandy, Gentleman", "Jane Eyre", "The Tenant of Wildfell Hall", "Villette"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
            
    def test_books_between_years_end_year_none(self):
        res = self.books_data_source.books_between_years(start_year=1900, end_year=None)
        bookTitleList = ["Main Street", "Elmer Gantry", "Murder on the Orient Express", "All Clear", "Blackout", "There, There"]
        
        for i in range(len(res)):
            assertEqual(res[i].title, bookTitleList[i])
