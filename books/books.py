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
    exit()
    
def usageError():
    print("Error: incorrect command")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()
    
def fileError():
    print("Error: csv_file_name must be a string ending with '.csv'")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()

def main():
    args = sys.argv
    if len(args)<2 or len(args)>8:
        argsNumError()
        
    
    if len(args)!=2: #It cannot be -h so there must be a file name
        if args[2][-4:]!='.csv':
            fileError()
        csv_file_name = args[2]
        search_text = args[3]
        if search_text=='None':
            search_text=None
        
    if args[1]=='-a' or args[1]=='--author':
        aspect1='None'
        aspect2='None'
        aspect3='None'
        aspect4='None'
        
        if len(args)<4 or len(args)>8:
            argsNumError()
    
        if len(args) >= 5:
            aspect1 = args[4]
        if len(args) >= 6:
            aspect2 = args[5]
        if len(args) >= 7:
            aspect3 = args[6]
        if len(args) == 8:
            aspect4 = args[7]
            
        source = booksdatasource.BooksDataSource(csv_file_name)
        res = source.authors(search_text=search_text)
        
        if aspect1 == 'None' and aspect2 == 'None' and aspect3 == 'None' and aspect4=='None':
            for author in res:
                s = 'Given name: '+author.given_name+'  Surname: '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['surname', 'None'] and aspect2 in ['surname', 'None'] and aspect3 in ['surname', 'None'] and aspect4 in ['surname', 'None']:
            for author in res:
                print('Surname:', author.surname)
        elif aspect1 in ['given_name', 'None'] and aspect2 in ['given_name', 'None'] and aspect3 in ['given_name', 'None'] and aspect4 in ['given_name', 'None']:
                print('Given name:', author.given_name)
        elif aspect1 in ['birth_year', 'None'] and aspect2 in ['birth_year', 'None'] and aspect3 in ['birth_year', 'None'] and aspect4 in ['birth_year', 'None']:
            for author in res:
                print('Birth:', author.birth_year)
        elif aspect1 in ['death_year', 'None'] and aspect2 in ['death_year', 'None'] and aspect3 in ['death_year', 'None'] and aspect4 in ['death_year', 'None']:
            for author in res:
                print(author.death_year)
        elif aspect1 in ['surname', 'given_name', 'None'] and aspect2 in ['surname', 'given_name', 'None'] and aspect3 in ['surname', 'given_name', 'None'] and aspect4 in ['surname', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Surname: '+author.surname
                print(s)
        elif aspect1 in ['birth_year', 'surname', 'None'] and aspect2 in ['birth_year', 'surname', 'None'] and aspect3 in ['birth_year', 'surname', 'None'] and aspect4 in ['birth_year', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Birth: '+str(author.birth_year)
                print(s)
        elif aspect1 in ['surname', 'death_year', 'None'] and aspect2 in ['surname', 'death_year', 'None'] and aspect3 in ['surname', 'death_year', 'None'] and aspect4 in ['surname', 'death_year', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'given_name', 'None'] and aspect2 in ['birth_year', 'given_name', 'None'] and aspect3 in ['birth_year', 'given_name', 'None'] and aspect4 in ['birth_year', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Birth: '+str(author.birth_year)
                print(s)
        elif aspect1 in ['death_year', 'given_name', 'None'] and aspect2 in ['death_year', 'given_name', 'None'] and aspect3 in ['death_year', 'given_name', 'None'] and aspect4 in ['death_year', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'None'] and aspect2 in ['birth_year', 'death_year', 'None'] and aspect3 in ['birth_year', 'death_year', 'None'] and aspect4 in ['birth_year', 'death_year', 'None']:
            for author in res:
                s = 'Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'given_name', 'surname', 'None'] and aspect2 in ['birth_year', 'given_name', 'surname', 'None'] and aspect3 in ['birth_year', 'given_name', 'surname', 'None'] and aspect4 in ['birth_year', 'given_name', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Given name: '+author.given_name+'  Birth: '+str(author.birth_year)
                print(s)
        elif aspect1 in ['death_year', 'given_name', 'surname', 'None'] and aspect2 in ['death_year', 'given_name', 'surname', 'None'] and aspect3 in ['death_year', 'given_name', 'surname', 'None'] and aspect4 in ['death_year', 'given_name', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Given name: '+author.given_name+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'surname', 'None'] and aspect2 in ['birth_year', 'death_year', 'surname', 'None'] and aspect3 in ['birth_year', 'death_year', 'surname', 'None'] and aspect4 in ['birth_year', 'death_year', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'given_name', 'None'] and aspect2 in ['birth_year', 'death_year', 'given_name', 'None'] and aspect3 in ['birth_year', 'death_year', 'given_name', 'None'] and aspect4 in ['birth_year', 'death_year', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'surname', 'given_name', 'None'] and aspect2 in ['birth_year', 'death_year', 'surname', 'given_name', 'None'] and aspect3 in ['birth_year', 'death_year', 'given_name', 'surname', 'None'] and aspect4 in ['birth_year', 'death_year', 'given_name', 'surname', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Surname: '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                
        else:
            usageError()
        
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
                argsNumError()
                
        sorted_by = args[4]
        
        if sorted_by!='title' and sorted_by!='year':
            usageError()

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
            usageError()
                    
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
                argsNumError()
        
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
            usageError()
        
    elif args[1]=='-h' or args[1]=='--help':
        file = open('usage.txt', 'r')
        lines = file.readlines()
        
        for line in lines:
            print(line)
    else:
        usageError()
    
    
if __name__ == "__main__":
    main()
