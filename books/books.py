'''
    books.py
    Yilong Song and Rodrick Lankford, 29 September 2021
    Command-line interface for booksdatasource.py
'''

import booksdatasource
import sys

def printArgsNumError():
    print("Error: incorrect number of arguments for books.py")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()
    
def printUsageError():
    print("Error: incorrect command")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()
    
def printFileError():
    print("Error: csv_file_name must be a string ending with '.csv'")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()

def printResult(res, print_surname_bool, print_given_name_bool, print_birth_year_bool, print_death_year_bool, print_title_bool, print_publication_year_bool, print_authors_bool):
    for item in res:
        s=''
        if print_given_name_bool:
            s+=('Given name: '+item.given_name+'  ')
        if print_surname_bool:
            s+=('Surname: '+item.surname+'  ')
        if print_birth_year_bool:
            s+=('Birth: '+str(item.birth_year)+'  ')
        if print_death_year_bool:
            s+=('Death: '+str(item.death_year)+'  ')
        if print_title_bool:
            s+=('Title: '+item.title+'  ')
        if print_publication_year_bool:
            s+=('Publication year: '+str(book.publication_year)+'  ')
        if print_authors_bool:
            s+='Authors'
            for author in item.authors:
                s+=author.given_name
                s+=' '
                s+=author.surname
                s+=', '
            s=s[:-2]
        s=s[:-2]
        print(s)
    

def main():
    args = sys.argv
    if len(args)<2 or len(args)>8:
        printArgsNumError()
        
    
    if len(args)!=2: #It cannot be -h so there must be a file name
        if args[2][-4:]!='.csv':
            printFileError()
        csv_file_name = args[2]
        search_text = args[3]
        if search_text=='None':
            search_text=None
        
    # Options for aspects: surname, given_name, birth_year, death_year
    print_surname_bool=False
    print_given_name_bool=False
    print_birth_year_bool=False
    print_death_year_bool=False
    print_title_bool=False
    print_publication_year_bool=False
    print_authors_bool=False
    
    if args[1]=='-a' or args[1]=='--author':
        if len(args)<4 or len(args)>8:
            printArgsNumError()
        
        aspects=args[4:]
        if len(aspects)==0:
            print_surname_bool=True
            print_given_name_bool=True
            print_birth_year_bool=True
            print_death_year_bool=True
            
        for aspect in aspects:
            if aspect=='surname':
                print_surname_bool=True
            elif aspect=='given_name':
                print_given_name_bool=True
            elif aspect=='birth_year':
                print_birth_year_bool=True
            elif aspect=='death_year':
                print_death_year_bool=True
            else:
                printUsageError()
        
        source = booksdatasource.BooksDataSource(csv_file_name)
        res=source.authors(search_text=search_text)
        
        printResult(res=res, print_surname_bool=print_surname_bool, print_given_name_bool=print_given_name_bool, print_birth_year_bool=print_birth_year_bool, print_death_year_bool=print_death_year_bool, print_title_bool=print_title_bool, print_publication_year_bool=print_publication_year_bool, print_authors_bool=print_authors_bool)
        
    elif args[1]=='-b' or args[1]=='--books':
        aspect1 = 'None'
        aspect2 = 'None'
        aspect3 = 'None'
        print(len(args))
        if len(args)!=5:
            if len(args)>=6:
                aspect1 = args[5]
            if len(args)>=7:
                aspect2 = args[6]
            if len(args)==8:
                aspect3 = args[7]
            if len(args)>8:
                printArgsNumError()
                
        sorted_by = args[4]
        
        if sorted_by!='title' and sorted_by!='year':
            printUsageError()

        source = booksdatasource.BooksDataSource(csv_file_name)
        res = source.books(search_text=search_text, sort_by=sorted_by)
        
        if aspect1=='None' and aspect2=='None' and aspect3=='None':
            for book in res:
                s='Title: '+book.title+'  Publication Year: '+str(book.publication_year)+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['title', 'None'] and aspect2 in ['title', 'None'] and aspect3 in ['title', 'None']:
            for book in res:
                s='Title: '+book.title
                print(s)
        elif aspect1 in ['publication_year', 'None'] and aspect2 in ['publication_year', 'None'] and aspect3 in ['publication_year', 'None']:
            for book in res:
                s='Publication year: '+str(book.publication_year)
                print(s)
        elif aspect1 in ['authors', 'None'] and aspect2 in ['authors', 'None'] and aspect3 in ['authors', 'None']:
            for book in res:
                s='Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['authors', 'title', 'None'] and aspect2 in ['authors', 'title', 'None'] and aspect3 in ['authors', 'title', 'None']:
            for book in res:
                s='Title: '+book.title+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['authors', 'publication_year', 'None'] and aspect2 in ['authors', 'publication_year', 'None'] and aspect3 in ['authors', 'publication_year', 'None']:
            for book in res:
                s='Publication year: '+str(book.publication_year)+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['publication_year', 'title', 'None'] and aspect2 in ['publication_year', 'title', 'None'] and aspect3 in ['publication_year', 'title', 'None']:
            for book in res:
                s='Title: '+book.title+'  Publication year: '+str(book.publication_year)
                print(s)
        elif aspect1 in ['authors', 'publication_year', 'title', 'None'] and aspect2 in ['authors', 'publication_year', 'title', 'None'] and aspect3 in ['authors', 'publication_year', 'title', 'None']:
            for book in res:
                s='Title: '+book.title+'  Publication Year: '+str(book.publication_year)+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        else:
            printUsageError()
                    
    elif args[1]=='-y' or args[1]=='--year':
        aspect1 = 'None'
        aspect2 = 'None'
        aspect3 = 'None'
        start_year = None
        end_year = None
        print(len(args))
        if len(args)!=5:
            if len(args)>=6:
                aspect1 = args[5]
            if len(args)>=7:
                aspect2 = args[6]
            if len(args)==8:
                aspect3 = args[7]
            if len(args)>8:
                printArgsNumError()
        
        if args[3]!='None':
            start_year=int(args[3])
        if args[4]!='None':
            end_year=int(args[4])

        source = booksdatasource.BooksDataSource(csv_file_name)
        res = source.books_between_years(start_year=start_year, end_year=end_year)
        
        if aspect1=='None' and aspect2=='None' and aspect3=='None':
            for book in res:
                s='Title: '+book.title+'  Publication Year: '+str(book.publication_year)+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['title', 'None'] and aspect2 in ['title', 'None'] and aspect3 in ['title', 'None']:
            for book in res:
                s='Title: '+book.title
                print(s)
        elif aspect1 in ['publication_year', 'None'] and aspect2 in ['publication_year', 'None'] and aspect3 in ['publication_year', 'None']:
            for book in res:
                s='Publication year: '+str(book.publication_year)
                print(s)
        elif aspect1 in ['authors', 'None'] and aspect2 in ['authors', 'None'] and aspect3 in ['authors', 'None']:
            for book in res:
                s='Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['authors', 'title', 'None'] and aspect2 in ['authors', 'title', 'None'] and aspect3 in ['authors', 'title', 'None']:
            for book in res:
                s='Title: '+book.title+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['authors', 'publication_year', 'None'] and aspect2 in ['authors', 'publication_year', 'None'] and aspect3 in ['authors', 'publication_year', 'None']:
            for book in res:
                s='Publication year: '+str(book.publication_year)+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        elif aspect1 in ['publication_year', 'title', 'None'] and aspect2 in ['publication_year', 'title', 'None'] and aspect3 in ['publication_year', 'title', 'None']:
            for book in res:
                s='Title: '+book.title+'  Publication year: '+str(book.publication_year)
                print(s)
        elif aspect1 in ['authors', 'publication_year', 'title', 'None'] and aspect2 in ['authors', 'publication_year', 'title', 'None'] and aspect3 in ['authors', 'publication_year', 'title', 'None']:
            for book in res:
                s='Title: '+book.title+'  Publication Year: '+str(book.publication_year)+'  Author(s): '
                for author in book.authors:
                    s+=author.given_name
                    s+=' '
                    s+=author.surname
                    s+=', '
                s=s[:-2]
                print(s)
        else:
            printUsageError()
        
    elif args[1]=='-h' or args[1]=='--help':
        file = open('usage.txt', 'r')
        lines = file.readlines()
        
        for line in lines:
            print(line)
    else:
        printUsageError()
    
    
if __name__ == "__main__":
    main()
