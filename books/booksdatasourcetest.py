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
        - general test
        - sort_by tests
            - 'year'
            - 'title'
            - default (same as 'title')
    (5 tests)
3) books_between_years(self, start_year=None, end_year=None)
    Features to check:
        - None for both test
        - general test
        - start_year = None test
        - end_year = None test
        - sorted by publication year, breaking ties by title
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
        res2 = self.books_data_source.books()
