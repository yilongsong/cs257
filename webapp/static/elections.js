/*
 * elections.js
 * Yilong Song, Skyler Kessenich
 * November 8, 2021
 */

window.onload = initialize;

function initialize() {

    let element = document.getElementById('search_button');
    if (element) {
        element.onclick = onCandidateSearchButtonPressed;
    }
}

// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}

function onCandidateSearchButtonPressed() {
    let searchString = document.getElementById('input_text').value
    let url = getAPIBaseURL() + '/candidate/' + searchString;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(candidateElectionHistory) {
        let displayBody = '';
        let startingYear = 0;
        let startingCandidate = '';

        // Deal with searches that yields no result
        if (candidateElectionHistory.length == 0) {
            displayBody += '<p class="display-candidate"> No candidate found!';
        }

        for (let k = 0; k < candidateElectionHistory.length; k++) {
            let election = candidateElectionHistory[k];
            // For every separate candidate
            if (election['candidate_name'] != startingCandidate) {
                displayBody += '</p>' + '<h2>' + election['candidate_name'] + '</h2>';
                startingCandidate= election['candidate_name']
                startingYear = 0;
            }

            // For every separate election
            if (election['year'] != startingYear) {
                displayBody += '</p>' + '<p class="display-candidate">'
                                + election['year'] + ' - '
                                + election['state'] + ' - ' 
                                + 'Party: ' + election['party'] + ' - '
                                + 'Votes Received: ' + String(election['votes_received'])
                                + '<br>' + 'Other candidates: ' + '<br>';
                startingYear = election['year'];
            }

            // Handeling other candidates
            displayBody += election['other_candidate_name'] 
                            + ' - ' + 'Votes Received: ' 
                            + String(election['other_candidate_votes_received']) + '<br>';
        }

        displayBody += '</p>'

        // Put the table body we just built inside the table that's already on the page.
        let electionHistoryOnPage = document.getElementById('candidate_election_history');
        if (electionHistoryOnPage) {
            electionHistoryOnPage.innerHTML = displayBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

