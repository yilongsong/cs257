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
    search_string_year = str(int(year))
    query = '''SELECT candidate.id, candidate.name, candidate.party, election.votes_received,
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
                        'candidate_party':row[2].lower().title(), 'votes_received':row[3], 'votes_total':row[4]}
            candidate_list.append(candidate)
        cursor.close()
        connection.close()
    except Exception as e:
        print(e, file=sys.stderr)
    
    return json.dumps(candidate_list)
    
@api.route('/election-results/for-candidate/<candidate_name>/')
def get_candidate_election_history(candidate_name):
    search_string = '%' + candidate_name.upper() + '%'
    query = '''SELECT DISTINCT c1.id, c1.name, c1.party, e1.year, state.state, e1.votes_received,
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
            candidate = {'candidate_id':row[0],
                        'candidate_name':row[1].lower().title(), 
                         'party':row[2].lower().title(), 'year':row[3],
                         'state':row[4].lower().title(), 'votes_received':row[5],
                         'other_candidate_name':row[6].lower().title(),
                         'other_candidate_votes_received':row[7]}
            candidate_list.append(candidate)
        cursor.close()
        connection.close()
        
        # Now determine if candidate by the name of candidate_name has won this election
        current_candidate = ''
        list_position = -1 # current position in the list
        for candidate in candidate_list:
            list_position += 1
            if current_candidate == candidate['candidate_name'] and current_year == candidate['year']:
                continue

            win_lose = 'Win'
            candidate_for_while_loop = candidate_list[list_position]
            list_position_for_while_loop = list_position
            while candidate_for_while_loop['candidate_name'] == candidate['candidate_name'] and candidate_for_while_loop['year'] == candidate['year']:
                if candidate_for_while_loop['votes_received'] < candidate_for_while_loop['other_candidate_votes_received']:
                    win_lose = 'Lose'
                if list_position_for_while_loop + 1 == len(candidate_list):
                    break
                list_position_for_while_loop += 1
                candidate_for_while_loop = candidate_list[list_position_for_while_loop]
            
            candidate['win_lose'] = win_lose
            current_candidate = candidate['candidate_name']
            current_year = candidate['year']


    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(candidate_list)

@api.route('/election-results/for-state/<state>/')
def get_state_election_history(state):
    search_string = '%' + state.upper() + '%'
    query = '''SELECT candidate.name, candidate.party, election.votes_received, election.year
                FROM candidate, election, state
                WHERE candidate.id = election.candidate_id AND election.state_id = state.id
                    AND state.state like %s
                ORDER BY election.year ASC, election.votes_received DESC;
            '''

    election_year_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_string,))
        current_year = 0 # To only get top two candidates per election year
        for row in cursor:
            if current_year != row[3]:
                current_year = row[3]
                candidate_count = 0
            
            if candidate_count == 2:
                continue

            if candidate_count < 2:
                election_year = {'candidate_name':row[0].lower().title(),
                                'candidate_party':row[1].lower().title(),
                                'votes_received':row[2], 'year':row[3]}
                election_year_list.append(election_year)
                candidate_count += 1
        cursor.close()
        connection.close()
    
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(election_year_list)


@api.route('/election-results/for-year/<year>/')
def get_year_election_history(year):
    search_string = str(int(year))
    query = '''SELECT candidate.name, candidate.party, election.votes_received, state.state
                FROM candidate, election, state
                WHERE candidate.id = election.candidate_id AND election.state_id = state.id
                    AND election.year = %s
                ORDER BY state.state ASC, election.votes_received DESC;
            '''
    election_year_list = []
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, (search_string,))
        current_state = '' # To only get top two candidates per state
        for row in cursor:
            if current_state != row[3]:
                current_state = row[3]
                candidate_count = 0
            
            if candidate_count == 2:
                continue

            if candidate_count < 2:
                election_year = {'candidate_name':row[0].lower().title(),
                                'candidate_party':row[1].lower().title(),
                                'votes_received':row[2], 'state':row[3].lower().title()}
                election_year_list.append(election_year)
                candidate_count += 1
        cursor.close()
        connection.close()
    
    except Exception as e:
        print(e, file=sys.stderr)

    return json.dumps(election_year_list)

@api.route('/help/')
def get_api_help():
    with open('static/api_documentation.txt', 'r') as f:
        document = f.read()
        return flask.Response(document, mimetype='text/plain')