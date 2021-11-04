'''
    books.py
    Yilong Song and Rodrick Lankford, 29 September 2021
    Command-line interface for booksdatasource.py
'''

import booksdatasource
import sys
#Function that throws error if the number of inputs are incorrect. 
def printArgsNumError():
    print("Error: incorrect number of arguments for books.py")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()
#Function that throws an error if the terminal input is not a registered command
def printUsageError():
    print("Error: incorrect command")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()
#Prints error message if the given file is incompatible    
def printFileError():
    print("Error: csv_file_name must be a string ending with '.csv'")
    print("Enter command 'python3 books.py -h' for Usage Manual")
    exit()
#Handels all the printings of the search aspects
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
            s+=('Publication year: '+str(item.publication_year)+'  ')
        if print_authors_bool:
            s+='Author(s): '
            for author in item.authors:
                s+=author.given_name
                s+=' '
                s+=author.surname
                s+=', '
            s=s[:-2]
        s=s[:-2]
        print(s)
    
#Imlementation of command interface using system args
def main():
    args = sys.argv
    
    # Check args length
    if len(args)<2 or len(args)>8:
        printArgsNumError()
        
    
    if len(args)!=2: #It cannot be -h so there must be a file name
        if args[2][-4:]!='.csv':
            printFileError()
        csv_file_name = args[2]
        search_text = args[3]
        if search_text=='None':
            search_text=None
        
    # Options for aspects: surname, given_name, birth_year, death_year, title, publication_year, authors
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
        if len(aspects)==0: # No aspect specified
            print_surname_bool=True
            print_given_name_bool=True
            print_birth_year_bool=True
            print_death_year_bool=True
        #determine what to search by    
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
        
    elif args[1]=='-b' or args[1]=='--books': # Works in similar way as -a case
        if len(args)<5 or len(args)>8:
            printArgsNumError()
        
        sort_by=args[4]
        if sort_by!='title' and sort_by!='year':
            printUsageError()
        
        aspects=args[5:]
        if len(aspects)==0:
            print_title_bool=True
            print_publication_year_bool=True
            print_authors_bool=True
        #check for title, publication_year, and authors aspect
        for aspect in aspects:
            if aspect=='title':
                print_title_bool=True
            elif aspect=='publication_year':
                print_publication_year_bool=True
            elif aspect=='authors':
                print_authors_bool=True
            else:
                printUsageError()
        
        source=booksdatasource.BooksDataSource(csv_file_name)
        res=source.books(search_text=search_text, sort_by=sort_by)
        
        printResult(res=res, print_surname_bool=print_surname_bool, print_given_name_bool=print_given_name_bool, print_birth_year_bool=print_birth_year_bool, print_death_year_bool=print_death_year_bool, print_title_bool=print_title_bool, print_publication_year_bool=print_publication_year_bool, print_authors_bool=print_authors_bool)

    #check for specified year                
    elif args[1]=='-y' or args[1]=='--year':
        start_year=None
        end_year=None
        
        if len(args)<5 or len(args)>8:
            printArgsNumError()
        
        if args[3]!='None':
            start_year=int(args[3])
        if args[4]!='None':
            end_year=int(args[4])
        
        aspects=args[5:]
        if len(aspects)==0:
            print_title_bool=True
            print_publication_year_bool=True
            print_authors_bool=True
        
        for aspect in aspects:
            if aspect=='title':
                print_title_bool=True
            elif aspect=='publication_year':
                print_publication_year_bool=True
            elif aspect=='authors':
                print_authors_bool=True
            else:
                printUsageError()
        
        source=booksdatasource.BooksDataSource(csv_file_name)
        res=source.books_between_years(start_year=start_year, end_year=end_year)
        
        printResult(res=res, print_surname_bool=print_surname_bool, print_given_name_bool=print_given_name_bool, print_birth_year_bool=print_birth_year_bool, print_death_year_bool=print_death_year_bool, print_title_bool=print_title_bool, print_publication_year_bool=print_publication_year_bool, print_authors_bool=print_authors_bool)
        
    
if __name__ == "__main__":
    main()
