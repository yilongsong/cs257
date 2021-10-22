'''
olympics.py

Yilong Song

USAGE
python3 olympics.py -h|--help                         prints a usage statement
python3 olympics.py -an|--athletesnoc noc             prints list of names of all the athletes from a specified NOC
python3 olympics.py -ng|--nocgold                     prints list of all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals
python3 olympics.py -am|--athletemedal athlete_name   prints list of medals a given athlete earned sorted by year earned
'''
import psycopg2
import sys

from config import password
from config import database
from config import user

def printArgsNumError():
    print("Error: incorrect number of arguments for books.py")
    print("Enter command 'python3 olympics.py -h' for Usage Manual")
    exit()

def main():
    args = sys.argv

    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()

    # check that number of arguments is within the acceptable range
    if len(args) < 2 or len(args) > 3:
        printArgsNumError()

    if args[1] == '-h' or args[1] == '--help':
        if len(args) != 2:
            printArgsNumError()
        
        usage_file = open('usage.txt', 'r')
        usage_file_lines = usage_file.readlines()

        for line in usage_file_lines:
            print(line)


    elif args[1] == '-an' or args[1] == '--athletesnoc':
        if len(args) != 3:
            printArgsNumError()
        
        query = "SELECT DISTINCT name FROM athletes, noc_regions WHERE athletes.noc_id = noc_regions.id AND noc_regions.noc='" + args[2] + "';"

        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()

        print("All athletes from", args[2], "NOC")
        print("=================================")
        for row in cursor:
            print(row[0])
        print()

    
    elif args[1] == '-ng' or args[1] == '--nocgold':
        if len(args) != 2:
            printArgsNumError()

        try:
            cursor = connection.cursor()
            query = "SELECT noc_regions.noc, count(athlete_event.id) FROM athletes, athlete_event, noc_regions WHERE athlete_event.athlete_id = athletes.id AND athlete_event.medal='Gold' AND athletes.noc_id = noc_regions.id GROUP BY noc_regions.noc ORDER BY count(athlete_event.athlete_id) DESC;"
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()
        
        print('NOC', '|', 'Number of Gold')
        print('================')
        for row in cursor:
            print(row[0], '|', row[1])
        print()

    elif args[1] == '-am' or args[1] == '--athletemedal':
        if len(args) != 3:
            printArgsNumError()
        athlete_name = '%'+args[2].replace(' ', '%'+'%')
        query = "SELECT events.year, athlete_event.medal FROM athletes, events, athlete_event WHERE athlete_event.athlete_id = athletes.id AND athlete_event.event_id = events.id AND athletes.name LIKE '" + athlete_name + "' AND athlete_event.medal!='NA'ORDER BY year ASC;"

        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()

        print("Medals earned by", args[2])
        print("==========================")
        for row in cursor:
            print(row[0], row[1])
        print()

if __name__ == '__main__':
    main()