'''
olympics-api.py
Yilong Song
October 26, 2021
'''

import psycopg2
import sys
import argparse
import flask
import json

from config import password
from config import database
from config import user

app = flask.Flask(__name__)

def get_connection():
    '''
    Get connection with databse
    '''
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()

    return connection

def get_cursor(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
        print(e)
        exit()

    return cursor


@app.route('/games')
def get_games():
    '''
    REQUEST: /games

    RESPONSE: a JSON list of dictionaries, each of which represents one
    Olympic games, sorted by year. Each dictionary in this list will have
    the following fields.

    id -- (INTEGER) a unique identifier for the games in question
    year -- (INTEGER) the 4-digit year in which the games were held (e.g. 1992)
    season -- (TEXT) the season of the games (either "Summer" or "Winter")
    city -- (TEXT) the host city (e.g. "Barcelona")
    '''
    connection = get_connection()
    query = 'SELECT distinct(year), season, city FROM events ORDER BY year ASC;'
    cursor = get_cursor(connection, query)

    list_dictionaries_games = []
    id = 1

    for row in cursor:
        dictionary_game = {}
        dictionary_game['id'] = id
        id+=1
        dictionary_game['year'] = row[0]
        dictionary_game['season'] = row[1]
        dictionary_game['city'] = row[2]
        list_dictionaries_games.append(dictionary_game)

    connection.close()
    
    return json.dumps(list_dictionaries_games)


@app.route('/nocs')
def get_noc():
    '''
    REQUEST: /nocs

    RESPONSE: a JSON list of dictionaries, each of which represents one
    National Olympic Committee, alphabetized by NOC abbreviation. Each dictionary
    in this list will have the following fields.

    abbreviation -- (TEXT) the NOC's abbreviation (e.g. "USA", "MEX", "CAN", etc.)
    name -- (TEXT) the NOC's full name (see the noc_regions.csv file)
    '''
    connection = get_connection()
    query = 'SELECT noc, region from noc_regions;'
    cursor = get_cursor(connection, query)

    list_dictionaries_noc = []

    for row in cursor:
        dictionary_noc = {}
        dictionary_noc['abbreviation'] = row[0]
        dictionary_noc['name'] = row[1]
        list_dictionaries_noc.append(dictionary_noc)

    connection.close()

    return json.dumps(list_dictionaries_noc)

@app.route('/medalists/games/<games_id>')
def get_medalists_games(games_id):
    '''
    REQUEST: /medalists/games/<games_id>?[noc=noc_abbreviation]

    RESPONSE: a JSON list of dictionaries, each representing one athlete
    who earned a medal in the specified games. Each dictionary will have the
    following fields.

    athlete_id -- (INTEGER) a unique identifier for the athlete
    athlete_name -- (TEXT) the athlete's full name
    athlete_sex -- (TEXT) the athlete's sex as specified in the database ("F" or "M")
    sport -- (TEXT) the name of the sport in which the medal was earned
    event -- (TEXT) the name of the event in which the medal was earned
    medal -- (TEXT) the type of medal ("gold", "silver", or "bronze")

    If the GET parameter noc=noc_abbreviation is present, this endpoint will return
    only those medalists who were on the specified NOC's team during the specified
    games.

    The <games_id> is whatever string (digits or otherwise) that your database/API
    uses to uniquely identify an Olympic games.
    '''
    connection = get_connection()
    noc_abbreviation = flask.request.args.get('noc')
    if noc_abbreviation != None:
        additional_query_part = " and noc_regions.noc = '" + noc_abbreviation + "' and noc_regions.id = athletes.noc_id"
    else:
        additional_query_part = ''
    query = """SELECT distinct(athletes.id), athletes.name, athletes.sex, events.sport, events.event, athlete_event.medal
    FROM athletes, events, athlete_event, noc_regions
    WHERE athlete_event.athlete_id = athletes.id and athlete_event.event_id = events.id and athlete_event.medal
    != 'NA' and events.id = """ + str(games_id) + additional_query_part+ ';'
    cursor = get_cursor(connection, query)

    list_dictionaries_athletes = []

    for row in cursor:
        dictionary_athletes = {}
        dictionary_athletes['athlete_id'] = row[0]
        dictionary_athletes['athlete_name'] = row[1]
        dictionary_athletes['athlete_sex'] = row[2]
        dictionary_athletes['sport'] = row[3]
        dictionary_athletes['event'] = row[4]
        dictionary_athletes['medal'] = row[5]
        list_dictionaries_athletes.append(dictionary_athletes)

    connection.close()

    return json.dumps(list_dictionaries_athletes)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('An Olympics data API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)