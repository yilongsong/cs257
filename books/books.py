'''
    books.py
    Yilong Song and Rodrick Lankford, 29 September 2021
    Command-line interface for booksdatasource.py
'''

import booksdatasource
import sys

def argsNumError():
    print("Error: incorrect number of arguments for books.py")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    
def usageError():
    print("Error: incorrect command")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    
def fileError():
    print("Error: csv_file_name must be a string ending with '.csv'")
    print("Enter command 'python3 books.py -h' for Usage Manual")

def main():
    args = sys.argv
    if len(args)<2 or len(args)>8:
        argsNumError()
        
    #['books.py', '-a', 'test.csv', 'search_text', 'aspect1', 'aspect2', 'aspect3', 'aspect4']

    #
    
    #
    
    if len(args)!=2: #It cannot be -h so there must be a file name
        if args[2][-4:]!='.csv':
            fileError()
        csv_file_name = args[2]
        
    if args[1]=='-a' or args[1]=='--author':
        search_text = None
        aspect = None
        if len(args)!=4:
            if len(args)==5:
                aspect = args[4]
            else:
                argsNumError()
            
        source = booksdatasource.BooksDataSource(csv_file_name)
        res = source.authors(search_text=search_text)
        
        if aspect == None:
            for author in res:
                s = 'Name: '+author.given_name+' '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect == 'surname':
            for author in res:
                print(author.surname)
        elif aspect == 'given_name':
            for author in res:
                print(author.given_name)
        elif aspect == 'birth_year':
            for author in res:
                print(author.birth_year)
        elif aspect == 'death_year':
            for author in res:
                print(author.death_year)
        else:
            usageError()
        
    elif args[1]=='-b' or args[1]=='--books':
        search_text = None
        aspect = None
        if len(args)!=5:
            if len(args)==6:
                aspect = args[5]
            else:
                argsNumError()
                
        sorted_by = args[4]

        source = booksdatasource.BooksDataSource(csv_file_name)
        res = source.books(search_text=search_text, sorted_by=sorted_by)
        
        if aspect == None:
            for book in res:
                s='Title: '+book.title+'  Publication Year: '+book.publication_year+'Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-1]
                print(s)
        elif aspect == 'title':
            for book in res:
                print(book.title)
        elif aspect == 'publication_year':
            for book in res:
                print(book.publication_year)
        elif aspect == 'authors':
            for book in res:
                for author in book.authors:
                    print(author.given_name, author.surname)
                    
    elif args[1]=='-y' or args[1]=='--year':
        pass
    elif args[1]=='-h' or args[1]=='--help':
        file = open('usage.txt', 'r')
        lines = file.readlines()
        
        for line in lines:
            print(line)
    else:
        usageError()
    
    
if __name__ == "__main__":
    main()
