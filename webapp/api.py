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

@api.route('/states/')
def get_states():
    query ='''SELECT state.id, state.state, state.state_po
            FROM state
            ORDER BY state.state;'''
    state_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            state = {'state_id':row[0], 'state_name':row[1].lower().title(), "state_po":row[2]}
            state_list.append(state)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    
    return json.dumps(state_list)

@api.route('/vote-total/state=<state>&year=<year>/')
def get_state_year_data(state, year):
    search_string_state = "'%" + state.upper()[1:-1] + "%'"
    search_string_year = year
    query = '''SELECT candidate.id, candidate.name, election.votes_received,
                election.votes_total
                FROM candidate, election, state
                WHERE candidate.id = election.candidate_id
                    AND election.state_id = state.id
                    AND state.state like %s
                    AND election.year = %s
                ORDER BY election.votes_received DESC;
    '''
    candidate_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query % (search_string_state, search_string_year))
        for row in cursor:
            candidate = {'candidate_id':row[0], 'candidate_name':row[1].lower().title(),
                        'votes_received':row[2], 'votes_total':row[3]}
            candidate_list.append(candidate)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    
    return json.dumps(candidate_list)
    
@api.route('/election-results/for-candidate/<candidate_name>/')
def get_candidate_election_history(candidate_name):
    search_string = '%' + candidate_name.upper() + '%'
    query = '''SELECT DISTINCT c1.name, c1.party, e1.year, state.state, e1.votes_received,
                    c2.name, e2.votes_received
                FROM candidate c1, candidate c2, election e1, election e2, state
                WHERE c1.id = e1.candidate_id AND c1.name like %s AND e1.state_id = state.id
                    AND e1.year = e2.year AND e1.state_id = e2.state_id AND c2.id = e2.candidate_id
                    AND c1.id != c2.id
                ORDER BY c1.name, e1.year DESC;'''

    candidate_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_string,))
        for row in cursor:
            candidate = {'candidate_name':row[0].lower().title(), 
                         'party':row[1].lower().title(), 'year':row[2],
                         'state':row[3].lower().title(), 'votes_received':row[4],
                         'other_candidate_name':row[5].lower().title(),
                         'other_candidate_votes_received':row[6]}
            candidate_list.append(candidate)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(candidate_list)

@api.route('/help/')
def get_api_help():
    with open('static/api_documentation.txt', 'r') as f:
        document = f.read()
        return flask.Response(document, mimetype='text/plain')