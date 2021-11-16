/*
 * elections.js
 * Yilong Song, Skyler Kessenich
 * November 8, 2021
 * 
 * @api.route('/vote-total/?state=<state>&year=<year>/')
 * @api.route('/election-results/for-candidate/<candidate_name>/')
 */

window.onload = initialize;

function initialize() {
    let stateYear = document.getElementById('state-year');
    let candidate = document.getElementById('candidate');
    
    if (stateYear && candidate) {
        stateYear.onclick = onSearchByStateYearButtonPressed
        candidate.onclick = onSearchByCandidateButtonPressed
    }
}

// For changing between functionalities
function deleteCandidateSearchElements() {
    let candidateSearchbox = document.getElementById('candidate-searchbox')
    if (candidateSearchbox) {
        candidateSearchbox.innerHTML = '';
    }
    let candidatesData = document.getElementById('candidate-election-history')
    if (candidatesData) {
        candidatesData.innerHTML = '';
    }
}

function deleteYearSearchElements() {;}

function deleteStateSearchElements() {;}

function deleteStateYearSearchElements() {
    let dropDowns = document.getElementById('state-year-drop-down')
    if (dropDowns) {
        dropDowns.innerHTML = '';
    }
    let pieChartTitle = document.getElementById('pie-chart-title')
    if (pieChartTitle) {
        pieChartTitle.innerHTML = '';
    }
    let pieChart = document.getElementById('pie-chart')
    if (pieChart) {
        pieChart.innerHTML = '';
    }
}

function deletePieChart() {
    let pieChart = document.getElementById('pie-chart')
    if (pieChart) {
        pieChart.innerHTML = '';
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

// Search by State & Year
function onSearchByStateYearButtonPressed() {
    // Delete other elements
    deleteCandidateSearchElements();
    deleteYearSearchElements();
    deleteStateSearchElements();
    deleteStateYearSearchElements();

    // Handle states
    let url = getAPIBaseURL()+ '/states/';
    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(states) {
        let state_year_selector = '';
        state_year_selector = '<p class="state-drop-down"><select id="state_selector">' +
                        '<option value="' + String(0) + '">' +
                        '--SELECT STATE--' + '</option>\n';
        for (let i = 0; i < states.length; i++) {
            let state = states[i];
            state_year_selector += '<option value="' + state['state_name'] + '">'
                            + state['state_name'] + '</option>\n';
        }

        state_year_selector += '</select></p>';
        
        // Handle years
        state_year_selector += '<p class="year-drop-down"><select id="year_selector">' +
                                '<option value="' + String(0) + '">' +
                                '--SELECT YEAR--' + '</option>\n';
        for (let i = 2020; i > 1975; i=i-2) {
            state_year_selector += '<option value="' + String(i) + '">'
                            + String(i) + '</option>\n';
        }

        state_year_selector += '</select></p>';

        // "GO" button
        state_year_selector += `<p class="go"><button><a class="button" id="search_button">
                                GO</a></button></p>`

        let selectorOnPage = document.getElementById('state-year-drop-down');
        if (selectorOnPage) {
            selectorOnPage.innerHTML = state_year_selector;
        }

        let searchButton = document.getElementById('search_button');
        if (searchButton) {
            searchButton.onclick = onStateYearSearchButtonPressed;
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

function onStateYearSearchButtonPressed() {
    deleteCandidateSearchElements();
    deleteYearSearchElements();
    deleteStateSearchElements();
    deletePieChart();

    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        let state = document.getElementById('state_selector').value;
        let year = document.getElementById('year_selector').value;
        let url = getAPIBaseURL() + '/vote-total/state='+ state + '&year=' + String(year) + '/';
        fetch(url, {method: 'get'})
        .then((response) => response.json())
        .then(function(pieChartData) {
            let data = [];
            data.push(['Candidate', 'Votes Received']);
            for (let k = 0; k < pieChartData.length; k++) {
                let candidate=pieChartData[k];
                let entry = [candidate['candidate_name'], candidate['votes_received']];
                data.push(entry);
            }

            let title = '<h2>% Votes Received for Candidates in ' + state + ' ' + year + '</h2>';
            let pieChartTitle = document.getElementById('pie-chart-title');
            if (pieChartTitle) {
                pieChartTitle.innerHTML = title;
            }

            if (pieChartData.length == 0) {
                if (pieChartTitle) {
                    if (state=='0' && year==0) {
                        pieChartTitle.innerHTML = '<p class="center">Please select a state and a year</p>';
                    } else {
                        pieChartTitle.innerHTML = '<p class="center">No Senate election occured for ' + state + ' in ' + year + '</p>';
                    }
                }
            } else {
                var googlePieChartData = google.visualization.arrayToDataTable(data);
                var chart = new google.visualization.PieChart(document.getElementById('pie-chart'));
                var options = {chartArea: {'left': 5, 'top': 5, 'right': 5},
                legend: {'position': 'bottom'},
                sliceVisibilityThreshold: .1};
 
                chart.draw(googlePieChartData, options);
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    }
}

// Search by Candidate
function onSearchByCandidateButtonPressed() {
    // Delete other elements
    deleteYearSearchElements();
    deleteStateSearchElements();
    deleteStateYearSearchElements();

    let url = getAPIBaseURL() + '/search-by-candidate/';
    let searchBox = `<input type="text" id="input_text" placeholder="Search by cadidate name">
    <button><a class="button" id="search_button">SEARCH</a></button>`
    
    let searchBoxOnPage = document.getElementById('candidate-searchbox')
    if (searchBoxOnPage) {
        searchBoxOnPage.innerHTML = searchBox;
    }

    let searchButton = document.getElementById('search_button');
    if (searchButton) {
        searchButton.onclick = onCandidateSearchButtonPressed;
    }

}

function onCandidateSearchButtonPressed() {
    let searchString = document.getElementById('input_text').value
    let url = getAPIBaseURL() + '/election-results/for-candidate/' + searchString;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(candidateElectionHistory) {
        let displayBody = '';
        let startingYear = 0;
        let startingCandidate = '';

        // Deal with searches that yields no result
        if (candidateElectionHistory.length == 0) {
            displayBody += '<p class="center"> No candidate found';
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

            // Handling other candidates
            displayBody += election['other_candidate_name'] 
                            + ' - ' + 'Votes Received: ' 
                            + String(election['other_candidate_votes_received']) + '<br>';
        }

        displayBody += '</p>'

        let electionHistoryOnPage = document.getElementById('candidate-election-history');
        if (electionHistoryOnPage) {
            electionHistoryOnPage.innerHTML = displayBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

// Search by State
function onSearchByStateButtonPressed() {}

function onStateSearchButtonPressed() {}

// Search by Year
function onSearchByYearButtonPressed() {}

function onYearSearchButtonPressed() {}