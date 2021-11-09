'''
    api.py
    Yilong Song, Skyler Kessenich
    November 8, 2021
'''
import sys
import flask
import json
import config
import psycopg2

api = flask.Blueprint('api', __name__)

def get_connection():
    return psycopg2.connect(database=config.database,
                            user=config.user,
                            password=config.password)

@api.route('/candidate/<candidate_name>')
def get_candidate_election_history(candidate_name):
    search_string = '%' + candidate_name.upper() + '%'
    query = '''SELECT candidate.name, candidate.party, election.votes_received, election.votes_total
                FROM candidate, election
                WHERE candidate.id = election.candidate_id AND candidate.name like %s;'''
    candidate_list = []

    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_string,))
        for row in cursor:
            candidate = {'name':row[0], 'party':row[1], 'votes_received':row[2], 'votes_total':row[3]}
            candidate_list.append(candidate)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(candidate_list)