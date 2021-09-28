#!/usr/bin/env python3
'''
    booksdatasource.py
    Jeff Ondich, 21 September 2021

    For use in the "books" assignment at the beginning of Carleton's
    CS 257 Software Design class, Fall 2021.
'''

import csv
from operator import itemgetter, attrgetter
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
#Alist = []

class BooksDataSource:
    Books = []
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
        
        #need to account for the casses of two first names or two last names
        
        with open(books_csv_file_name) as csv_file:
            read = csv.reader(csv_file, delimiter=',')
            for line in read:
                alist = []
                aInfo = line[2].split(' ')
                given_name = aInfo[0]
                if (aInfo[2].isalpha()) & (aInfo[2] != 'and'):
                    surname = aInfo[2]
                    birth_info = (aInfo[3].replace("(","").replace(")","").replace("-"," ")).split(' ')
                    birth_year = birth_info[0]
                else:
                    surname = aInfo[1]
                    birth_info = (aInfo[2].replace("(","").replace(")","").replace("-"," ")).split(' ')
                    birth_year = birth_info[0]
                
                
                if 'and' in line[2]:
                    surname2 = aInfo[-2]
                    if (aInfo[-4] != 'and'):                        
                        given_name2 = aInfo[-4]
                    else:
                        given_name2 = aInfo[-3]
                    birth_info2 = (aInfo[-1].replace("(","").replace(")","").replace("-"," ")).split(' ')
                    birth_year2 = birth_info2[0]
                    #not needed
                    if len(birth_info2) < 2:
                        death_year2 = None
                    else:
                        death_year2 = birth_info2[1]
                    author2 = Author(surname=surname2,given_name=given_name2,birth_year=birth_year2,death_year=death_year2)
                    alist.append(author2)
                book_title = line[0]
                book_year = line[1]
                #not needed
                if len(birth_info) < 2:
                    death_year = None
                else:
                    death_year = birth_info[1]
                author1 = Author(surname=surname,given_name=given_name,birth_year=birth_year,death_year=death_year)
                alist.append(author1)
                #author2 = Author(surname=surname2,given_name=given_name2,birth_year=birth_year2,death_year=death_year2)
                #alist.append(author2)

                book = Book(title=book_title,publication_year=book_year,authors=alist)
                self.Books.append(book)
                
                
        #pass
    #need to make a sort function
    def ysort(self, sort=''):
        # author_objects = books.authors
        # sorted(author_objects, key=attrgetter('surname'))


        #if sort == "year":
        sorted(self.Books,key=attrgetter("publication_year"))

        return []
        

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        Alist = []
        #for ath in books:
            #print(ath.authors[0].surname)
        #self.sort("name")
        #search_text = "Haruki"
        
        for bk in self.Books:
            for ath in bk.authors:
                if (search_text == ath.surname) | (search_text == ath.given_name):
                    Alist.append(ath)
                             
                if (search_text == None):
                    #print(ath.surname)
                    Alist.append(ath)
        #sorted(Alist,key=attrgetter("surname"))
        Alist.sort(key=lambda x: (x.surname, x.given_name))
        #print(Alist[0].surname  )

        return Alist

    def books(self, search_text=None, sort_by='title'):
        ''' Returns a list of all the Book objects in this data source whose
            titles contain (.case-insensitively) search_text. If search_text is None,
            then this method returns all of the books objects.

            The list of books is sorted in an order depending on the sort_by parameter:

                'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
                'title' -- sorts by (case-insensitive) title, breaking ties with publication_year
                default -- same as 'title' (that is, if sort_by is anything other than 'year'
                            or 'title', just do the same thing you would do for 'title')
        '''
        Blist = []
        
        for bk in self.Books:
            t = bk.title
            if (search_text in  bk.title):
                Alist.append(bk)
                            
            if (search_text == None):
                #print(ath.surname)
                Alist.append(bk)
        #sorted(Alist,key=attrgetter("surname"))
        if (sort_by == 'title'):
            Blist.sort(key=lambda x: (x.title))
        if (sort_by == 'year'):
            Blist.sort(key=lambda x: (x.year))
        else:
            Blist.sort(key=lambda x: (x.title))
        return Blist

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
#for minor test
def main():
    b = BooksDataSource("book1.csv")

    b.authors()
    
    # arguments = parse_command_line()
    # if len(sys.argv) == 2:
    #     arguments('person-name') =sys.argv[1]
    # else:
    #     main(arguments)
if __name__ == "__main__":
    main()
