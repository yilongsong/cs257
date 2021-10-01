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
        search_text = args[3]
        
    if args[1]=='-a' or args[1]=='--author':
        aspect1='None'
        aspect2='None'
        aspect3='None'
        if len(args)<4 or len(args)>7:
            argsNumError()
    
        if len(args) >= 5:
            aspect1 = args[4]
        if len(args) >= 6:
            aspect2 = args[5]
        if len(args) == 7:
            aspect3 = args[6]
            
        source = booksdatasource.BooksDataSource(csv_file_name)
        res = source.authors(search_text=search_text)
        
        if aspect1 == 'None' and aspect2 == 'None' and aspect3 == 'None':
            for author in res:
                s = 'Given name: '+author.given_name+'  Surname: '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['surname', 'None'] and aspect2 in ['surname', 'None'] and aspect3 in ['surname', 'None']:
            for author in res:
                print('Surname:', author.surname)
        elif aspect1 in ['given_name', 'None'] and aspect2 in ['given_name', 'None'] and aspect3 in ['given_name', 'None']:
                print('Given name:', author.given_name)
        elif aspect1 in ['birth_year', 'None'] and aspect2 in ['birth_year', 'None'] and aspect3 in ['birth_year', 'None']:
            for author in res:
                print('Birth:', author.birth_year)
        elif aspect1 in ['death_year', 'None'] and aspect2 in ['death_year', 'None'] and aspect3 in ['death_year', 'None']:
            for author in res:
                print(author.death_year)
        elif aspect1 in ['surname', 'given_name', 'None'] and aspect2 in ['surname', 'given_name', 'None'] and aspect3 in ['surname', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Surname: '+author.surname
                print(s)
        elif aspect1 in ['birth_year', 'surname', 'None'] and aspect2 in ['birth_year', 'surname', 'None'] and aspect3 in ['birth_year', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Birth: '+str(author.birth_year)
                print(s)
        elif aspect1 in ['surname', 'death_year', 'None'] and aspect2 in ['surname', 'death_year', 'None'] and aspect3 in ['surname', 'death_year', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'given_name', 'None'] and aspect2 in ['birth_year', 'given_name', 'None'] and aspect3 in ['birth_year', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Birth: '+str(author.birth_year)
                print(s)
        elif aspect1 in ['death_year', 'given_name', 'None'] and aspect2 in ['death_year', 'given_name', 'None'] and aspect3 in ['death_year', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'None'] and aspect2 in ['birth_year', 'death_year', 'None'] and aspect3 in ['birth_year', 'death_year', 'None']:
            for author in res:
                s = 'Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'given_name', 'surname', 'None'] and aspect2 in ['birth_year', 'given_name', 'surname', 'None'] and aspect3 in ['birth_year', 'given_name', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Given name: '+author.given_name+'  Birth: '+str(author.birth_year)
                print(s)
        elif aspect1 in ['death_year', 'given_name', 'surname', 'None'] and aspect2 in ['death_year', 'given_name', 'surname', 'None'] and aspect3 in ['death_year', 'given_name', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Given name: '+author.given_name+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'surname', 'None'] and aspect2 in ['birth_year', 'death_year', 'surname', 'None'] and aspect3 in ['birth_year', 'death_year', 'surname', 'None']:
            for author in res:
                s = 'Surname: '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'given_name', 'None'] and aspect2 in ['birth_year', 'death_year', 'given_name', 'None'] and aspect3 in ['birth_year', 'death_year', 'given_name', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                print(s)
        elif aspect1 in ['birth_year', 'death_year', 'surname', 'given_name', 'None'] and aspect2 in ['birth_year', 'death_year', 'surname', 'given_name', 'None'] and aspect3 in ['birth_year', 'death_year', 'given_name', 'surname', 'None']:
            for author in res:
                s = 'Given name: '+author.given_name+'  Surname: '+author.surname+'  Birth: '+str(author.birth_year)+'  Death: '+str(author.death_year)
                
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
