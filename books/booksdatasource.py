#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
    
    Four Functions implemented by Yilong Song and Rodrick Lankford
'''

import csv

class Author:
    def __init__(self, surname='', given_name='', birth_year=None, death_year=None):
        self.surname = surname
        self.given_name = given_name
        self.birth_year = birth_year
        self.death_year = death_year

class Book:
    def __init__(self, title='', publication_year=None, authors=[]):
        ''' Note that the self.authors instance variable is a list of
            references to Author objects. '''
        self.title = title
        self.publication_year = publication_year
        self.authors = authors

class BooksDataSource:
    def __init__(self, books_csv_file_name):
        ''' The books CSV file format looks like this:

                title,publication_year,author_description

            For example:

                All Clear,2010,Connie Willis (1945-)
                "Right Ho, Jeeves",1934,Pelham Grenville Wodehouse (1881-1975)

            This __init__ method parses the specified CSV file and creates
            suitable instance variables for the BooksDataSource object containing
            a collection of Author objects and a collection of Book objects.
        '''
        self.books = []
        self.authors = []
        
        file = open(books_csv_file_name, 'r')
        reader = file.readlines()
        for line in reader:
            book_info = line.replace(" (", ",").replace(")", "").replace("-", ",").replace("\n",'')
            
            if book_info[0] == '\"':
                list1 = book_info.split('"')
                list2 = list1[2].split(",")
                book_info_list = []
                book_info_list.append(list1[1])
                book_info_list.append(list2[1])
                book_info_list.append(list2[2])
                book_info_list.append(list2[3])
                book_info_list.append(list2[4])
            else:
                book_info_list = book_info.split(",")
            
            print(book_info_list) #for debugging purposes
            
            name = book_info_list[2]
            name_list = name.split(" ")
            
            if (book_info_list[-1]) == '':
                book_info_list[-1] = None
            
            authors = Author(name_list[0], name_list[-1], book_info_list[3], book_info_list[4])
            
            book = Book(book_info_list[0], book_info_list[1], [authors])
            
            for i in range(len(self.authors)): #check if author already exists in collection
                if (authors.surname == self.authors[i].surname and authors.given_name == self.authors[i].given_name):
                    break
                if i == len(self.authors)-1:
                    self.authors.append(author)
            self.books.append(book)
            

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        return []

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        return []

    def books_between_years(self, start_year=None, end_year=None):
        ''' Returns a list of all the Book objects in this data source whose publication
            years are between start_year and end_year, inclusive. The list is sorted
            by publication year, breaking ties by title (e.g. Neverwhere 1996 should
            come before Thief of Time 1996).

            If start_year is None, then any book published before or during end_year
            should be included. If end_year is None, then any book published after or
            during start_year should be included. If both are None, then all books
            should be included.
        '''
        return []


def main():
    test = BooksDataSource('books1.csv')
    
if __name__=='__main__':
    main()
