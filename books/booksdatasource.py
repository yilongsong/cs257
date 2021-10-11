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
        self.books_collection = []
        self.authors_collection = []
        
        file = open(books_csv_file_name, 'r')
        reader = csv.reader(file)
        
        for row in reader:
            # for construction of each book object
            book_title = row[0]
            book_publication_year = int(row[1])
            authors_list = []
            
            # for construction of each author object
            author_info = row[2].replace(" (", ",").replace(")", "").replace("-", ",").replace("\n",'').replace(' and ', ',')
            author_info_list = author_info.split(",")
            
            #for each author of the book
            n = 0
            for i in range(len(author_info_list)//3):
                author_name = author_info_list[n]
                author_birth_year = int(author_info_list[n+1])
                author_death_year = author_info_list[n+2]
                if author_death_year == '':
                    author_death_year = None
                else:
                    author_death_year = int(author_death_year)
                    
                #author must have a none void birth year
                 
                author_name_list = author_name.split(" ")
                author_given_name = author_name_list[0]
                author_surname = author_name_list[-1]
                
                author = Author(surname=author_surname, given_name=author_given_name, birth_year=author_birth_year, death_year=author_death_year)
                
                if len(self.authors_collection)==0:
                    self.authors_collection.append(author)
                    
                for j in range(len(self.authors_collection)): #check if author already exists in collection
                    if (author.surname == self.authors_collection[j].surname and author.given_name == self.authors_collection[j].given_name):
                        break
                    if j == len(self.authors_collection)-1:
                        self.authors_collection.append(author)
                
                authors_list.append(author)

                n+=3
                
            # finish constructing each book object
            book = Book(title = book_title, publication_year=book_publication_year, authors=authors_list)
            self.books_collection.append(book)

    def authors(self, search_text=None):
        ''' Returns a list of all the Author objects in this data source whose names contain
            (case-insensitively) the search text. If search_text is None, then this method
            returns all of the Author objects. In either case, the returned list is sorted
            by surname, breaking ties using given name (e.g. Ann Brontë comes before Charlotte Brontë).
        '''
        res = []
        #Search for author the is set by search parameter, or searches all the authors if parameter is None
        for author in self.authors_collection:
            if search_text==None or (search_text.lower() in author.surname.lower()) or (search_text.lower() in author.given_name.lower()):
                res.append(author)
            
        res.sort(key=lambda x: (x.surname, x.given_name))
        
        return res

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
        res = []
        #Search for desired book
        for book in self.books_collection:
            if search_text==None or (search_text.lower() in book.title.lower()):
                res.append(book)
        #Sort dependent on sort_by parameter
        if sort_by=='year':
            res.sort(key=lambda x: (x.publication_year, x.title))
        else:
            res.sort(key=lambda x: (x.title, x.publication_year))
        
        return res

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
        res = []
      
        for book in self.books_collection:
            if start_year==None and end_year==None:
                res.append(book)
            elif start_year==None:
                if book.publication_year <= end_year:
                    res.append(book)
            elif end_year==None:
                if book.publication_year >= start_year:
                    res.append(book)
            else:
                if book.publication_year >= start_year and book.publication_year <= end_year:
                    res.append(book)
        
        res.sort(key=lambda x: (x.publication_year, x.title))
        
        return res


def main():
    #Implement test cases for the book database
    test = BooksDataSource('test.csv')
    testauthorlist = test.books(search_text='TH')
    for item in testauthorlist:
        print(item.title)
    
if __name__=='__main__':
    main()
