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
    let year = document.getElementById('year');
    let state = document.getElementById('state');
    
    if (stateYear && candidate) {
        stateYear.onclick = onSearchByStateYearButtonPressed;
        candidate.onclick = onSearchByCandidateButtonPressed;
        state.onclick = onSearchByStateButtonPressed;
        year.onclick = onSearchByYearButtonPressed;
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

function deleteYearSearchElements() {
    let dropDowns = document.getElementById('unique-drop-down')
    if (dropDowns) {
        dropDowns.innerHTML = '';
    }
}

function deleteStateSearchElements() {
    let dropDowns = document.getElementById('unique-drop-down')
    if (dropDowns) {
        dropDowns.innerHTML = '';
    }
    let columnChartTitle = document.getElementById('column-chart-title')
    if (columnChartTitle) {
        columnChartTitle.innerHTML = '';
    }
    let columnChart = document.getElementById('column-chart')
    if (columnChart) {
        columnChart.innerHTML = '';
    }
    let columnChartText = document.getElementById('column-chart-text')
    if (columnChartText) {
        columnChartText.innerHTML = '';
    }
}

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
                let candidateNameParty = candidate['candidate_name'] + ' (' + candidate['candidate_party'] + ')';
                let entry = [candidateNameParty, candidate['votes_received']];
                data.push(entry);
            }

            let title = '<h2>% Votes Received for Candidates in ' + state + ' ' + year + '</h2>';
            let pieChartTitle = document.getElementById('pie-chart-title');
            if (pieChartTitle) {
                pieChartTitle.innerHTML = title;
            }

            if (pieChartData.length == 0 || (state == 0 || year == 0)) {
                if (pieChartTitle) {
                    if (state == 0 && year==0) {
                        pieChartTitle.innerHTML = '<p class="center">Please select a state and a year</p>';
                    } else if (state == 0) {
                        pieChartTitle.innerHTML = '<p class="center">Please select a state</p>';
                    } else if (year == 0) {
                        pieChartTitle.innerHTML = '<p class="center">Please select a year</p>';
                    } else {
                        pieChartTitle.innerHTML = '<p class="center">No Senate election occured for ' + state + ' in ' + year + '</p>';
                    }
                }
            } else {
                var googlePieChartData = google.visualization.arrayToDataTable(data);
                var chart = new google.visualization.PieChart(document.getElementById('pie-chart'));
                var options = {chartArea: {'left': 5, 'top': 5, 'right': 5},
                legend: {'position': 'bottom'},
                sliceVisibilityThreshold: .1,
                colors: ['orange', 'purple', 'green', 'cyan', 'magenta']};
 
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
    deleteStateSearchElements();

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
        let candidateCount = 0;
        const candidateNameList = [];

        // Deal with searches that yields no result
        if (candidateElectionHistory.length == 0) {
            displayBody += '<p class="center"> No candidate found</p>';
        } else {
            // Display a list of candidates
            displayBody += '<p class="center">Click a candidate name to view their full election history</p>'
            displayBody += `<table class="candidate-name-display">
                            <tr><td class="bold-and-underline">Candidate Name</td>
                            <td class="bold-and-underline">Party</td></tr>`
            for (let k = 0; k < candidateElectionHistory.length; k++) {
                let election = candidateElectionHistory[k];
                // For every separate candidate (first 50)
                if (election['candidate_name'] != startingCandidate && candidateCount < 50) {
                    displayBody += `<tr><td><a class="candidate-name" id='` 
                                    + election['candidate_name'] + `' value='` +
                                    election['candidate_name'] + `' onclick='onCandidateNameButtonPressed(&#39;` + 
                                    election['candidate_name'] + `&#39;)'>` +
                                    election['candidate_name'] + `</a></td><td>` +
                                    election['party'] + `</td>`;
                }
                // Keep counting past 50
                if (election['candidate_name'] != startingCandidate) {
                    startingCandidate = election['candidate_name'];
                    candidateNameList[candidateCount] = election['candidate_name'];
                    candidateCount++;
                }
            }
            displayBody += '</table>'
            if (candidateCount >= 50) {
                displayBody += '<p class="center">' + String(candidateCount) 
                            + ` candidates found. Displaying first 50. Enter more specified search
                            string to narrow result.</p>\n<a class="show-all" id="show-all">
                            SHOW FULL RESULT</a>`;
                            
            }
        }

        // Put displayBody into html
        let electionHistoryOnPage = document.getElementById('candidate-election-history');
        if (electionHistoryOnPage) {
            electionHistoryOnPage.innerHTML = displayBody;
        }

        // Handle when user presses "SHOW FULL RESULT"
        let showFullResultButton = document.getElementById('show-all') 
        if (showFullResultButton) {
            showFullResultButton.onclick = onShowFullCandidateSearchResultButtonPressed;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

// Show election result of invidual candidate when that candidate's name is clicked
function onCandidateNameButtonPressed(value) {
    let searchString = value;
    let url = getAPIBaseURL() + '/election-results/for-candidate/' + searchString;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(candidateElectionHistory) {
        let displayBody = '';
        let startingYear = 0;
        let startingCandidate = '';

        // Deal with searches that yields no result
        if (candidateElectionHistory.length == 0) {
            displayBody += '<p class="center"> No candidate found</p>';
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
                                + ' - ' + election['win_lose']
                                + '<br>' + 'Other candidates: ' + '<br>';
                startingYear = election['year'];
            }

            // Handling other candidates
            displayBody += election['other_candidate_name'] 
                            + ' - ' + 'Votes Received: ' 
                            + String(election['other_candidate_votes_received']) + '<br>';
        }

        displayBody += `</p><p class="back-button"><button><a class="button" id="back_button"
                        >BACK</a></button></p>`

        let electionHistoryOnPage = document.getElementById('candidate-election-history');
        if (electionHistoryOnPage) {
            electionHistoryOnPage.innerHTML = displayBody;
        }

        let backButton = document.getElementById('back_button');
        if (backButton) {
            backButton.onclick = onCandidateSearchButtonPressed;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

// Show full candidate search result upon request
function onShowFullCandidateSearchResultButtonPressed() {
    let searchString = document.getElementById('input_text').value
    let url = getAPIBaseURL() + '/election-results/for-candidate/' + searchString;

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(candidateElectionHistory) {
        let displayBody = '';
        let startingCandidate = '';

        // Deal with searches that yields no result
        if (candidateElectionHistory.length == 0) {
            displayBody += '<p class="center"> No candidate found</p>';
        }

        // Display a list of candidates
        displayBody += '<p class="center">Click a candidate name to view their full election history</p>'
        displayBody += `<table class="candidate-name-display">
                        <tr><td class="bold-and-underline">Candidate Name</td>
                        <td class="bold-and-underline">Party</td></tr>`
        for (let k = 0; k < candidateElectionHistory.length; k++) {
            let election = candidateElectionHistory[k];
            // For every separate candidate
            if (election['candidate_name'] != startingCandidate) {
                displayBody += `<tr><td><a class="candidate-name" id='` 
                + election['candidate_name'] + `' value='` +
                election['candidate_name'] + `' onclick='onCandidateNameButtonPressed(&#39;` + 
                election['candidate_name'] + `&#39;)'>` +
                election['candidate_name'] + `</a></td><td>` +
                election['party'] + `</td>`;
                startingCandidate = election['candidate_name'];
            }
        }
        displayBody += '</table>';

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
function onSearchByStateButtonPressed() {
    // Delete other elements
    deleteStateSearchElements();
    deleteCandidateSearchElements();
    deleteStateYearSearchElements();

    let url = getAPIBaseURL() + '/states/';
    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(states) {
        let state_selector = '';
        state_selector = '<p class="unique-drop-down"><select id="state_selector">' +
                        '<option value="' + String(0) + '">' +
                        '--SELECT STATE--' + '</option>\n';
        for (let i = 0; i < states.length; i++) {
            let state = states[i];
            state_selector += '<option value="' + state['state_name'] + '">'
                            + state['state_name'] + '</option>\n';
        }

        state_selector+= '</select></p>';

        // "GO" button
        state_selector += `<p class="go"><button><a class="button" id="search_button">
                            GO</a></button></p>`

        let selectorOnPage = document.getElementById('unique-drop-down');
        if (selectorOnPage) {
            selectorOnPage.innerHTML = state_selector;
        }

        let searchButton = document.getElementById('search_button');
        if (searchButton) {
            searchButton.onclick = onStateSearchButtonPressed;
        }
    })
    .catch(function(error) {
        console.log(error);
    });
}

function onStateSearchButtonPressed() {
    deleteCandidateSearchElements();
    deleteStateYearSearchElements();
    deletePieChart();

    google.charts.load('current', {'packages':['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        let state = document.getElementById('state_selector').value;
        let url = getAPIBaseURL() + '/election-results/for-state/' + state + '/';
        fetch(url, {method: 'get'})
        .then((response) => response.json())
        .then(function(columnChartData) {
            let data = [];
            let tableData = []
            data.push(['Year', 'Winner Votes Received', 'Runner-up Votes Received']);
            // In pairs
            for (let k = 0; k < columnChartData.length; k=k+2) {
                let candidate1 = columnChartData[k];
                let candidateNameParty1 = candidate1['candidate_name'] + ' (' + candidate1['candidate_party']
                                        + ')';
                let candidate2 = columnChartData[k+1];
                if (k+1 >= columnChartData.length) {
                    candidate2 = {'candidate_name': '', 'votes_received': 0};
                }

                if (candidate1['year']==2021) {
                    break;
                }
                let candidateNameParty2 = candidate2['candidate_name'] + ' (' + candidate2['candidate_party']
                                        + ')';
                let entry = [String(candidate1['year']),
                             candidate1['votes_received'], candidate2['votes_received']];
                data.push(entry);

                let tableEntry = [String(candidate1['year']), candidateNameParty1, candidateNameParty2];
                tableData.push(tableEntry);
            }

            var options = {
                width: 1250,
                height: 600
              };
      

            let title = '<h2> Votes Received for Candidates in ' + state + ' 1976-2020</h2>';
            let columnChartTitle = document.getElementById('column-chart-title');
            if (columnChartTitle) {
                columnChartTitle.innerHTML = title;
            }

            if (columnChartData.length == 0) {
                if (columnChartTitle) {
                    columnChartTitle.innerHTML = '<p class="center">Please select a state</p>';
                }
            } else {
                var googleColumnChartData = google.visualization.arrayToDataTable(data);
                var chart = new google.charts.Bar(document.getElementById('column-chart'));
                chart.draw(googleColumnChartData, google.charts.Bar.convertOptions(options))
            }

            displayBody = '<br><br><table class="column-chart-text">';
            displayBody += '<tr>' + '<td class=bold-and-underline>Year:</td>';
            for (i = 0; i < tableData.length; i++) {
                displayBody +=  '<td>' + tableData[i][0] + '</td>';
            }
            displayBody += '</tr>';

            displayBody += '<tr>' + '<td class=bold-and-underline>Winner:</td>';
            for (i = 0; i < tableData.length; i++) {
                displayBody +=  '<td>' + tableData[i][1] + '</td>';
            }
            displayBody += '</tr>';

            displayBody += '<tr>' + '<td class=bold-and-underline>Runner-up:</td>';
            for (i = 0; i < tableData.length; i++) {
                displayBody +=  '<td>' + tableData[i][2] + '</td>';
            }
            displayBody += '</tr>';
            displayBody += '</table>';

            let columnChartHTML = document.getElementById('column-chart-text');
            if (columnChartHTML) {
                columnChartHTML.innerHTML = displayBody;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    }


}

// Search by Year
function onSearchByYearButtonPressed() {
    deleteCandidateSearchElements();
    deleteStateSearchElements();
    deleteStateYearSearchElements();

    let year_selector = '<p class="unique-drop-down"><select id="year_selector">' +
                        '<option value="' + String(0) + '">' +
                        '--SELECT YEAR--' + '</option>\n';
    for (let i = 2020; i > 1975; i=i-2) {
        year_selector += '<option value="' + String(i) + '">'
                        + String(i) + '</option>\n';
    }

    year_selector += '</select></p>';
    // "GO" button
    year_selector += `<p class="go"><button><a class="button" id="search_button">
    GO</a></button></p>`

    let selectorOnPage = document.getElementById('unique-drop-down');
    if (selectorOnPage) {
        selectorOnPage.innerHTML = year_selector;
    }

    let searchButton = document.getElementById('search_button');
    if (searchButton) {
        searchButton.onclick = onYearSearchButtonPressed;
    }
}

function onYearSearchButtonPressed() {
    deleteCandidateSearchElements();
    deleteStateYearSearchElements();
    deletePieChart();

    google.charts.load('current', {'packages':['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        let year = document.getElementById('year_selector').value;
        let url = getAPIBaseURL() + '/election-results/for-year/' + String(year) + '/';
        fetch(url, {method: 'get'})
        .then((response) => response.json())
        .then(function(columnChartData) {
            let data = [];
            let tableData = []
            data.push(['State', 'Winner Votes Received', 'Runner-up Votes Received']);
            // In pairs
            for (let k = 0; k < columnChartData.length; k=k+2) {
                let candidate1 = columnChartData[k];
                let candidateNameParty1 = candidate1['candidate_name'] + ' (' + candidate1['candidate_party']
                                        + ')';
                let candidate2 = columnChartData[k+1];

                if (candidate1['state'] != candidate2['state']) {
                    k = k-1;
                    continue;
                }

                if (k+1 >= columnChartData.length) {
                    candidate2 = {'candidate_name': '', 'votes_received': 0};
                }

                let candidateNameParty2 = candidate2['candidate_name'] + ' (' + candidate2['candidate_party']
                                        + ')';
                let entry = [String(candidate1['state']),
                             candidate1['votes_received'], candidate2['votes_received']];
                data.push(entry);

                let tableEntry = [String(candidate1['state']), candidateNameParty1, candidateNameParty2];
                tableData.push(tableEntry);
            }

            var options = {
                width: 1850,
                height: 600
              };
      

            let title = '<h2> Votes Received for Candidates in ' + String(year) + ' (All States where Election Occured)</h2>';
            let columnChartTitle = document.getElementById('column-chart-title');
            if (columnChartTitle) {
                columnChartTitle.innerHTML = title;
            }

            if (columnChartData.length == 0) {
                if (columnChartTitle) {
                    columnChartTitle.innerHTML = '<p class="center">Please select a year</p>';
                }
            } else {
                var googleColumnChartData = google.visualization.arrayToDataTable(data);
                var chart = new google.charts.Bar(document.getElementById('column-chart'));
                chart.draw(googleColumnChartData, google.charts.Bar.convertOptions(options))
            }

            displayBody = '<br><br><table class="column-chart-text-center">';
            displayBody += `<tr><td class=bold-and-underline>State</td>
                            <td class=bold-and-underline>Winner</td>
                            <td class=bold-and-underline>Runner-up</td></tr>`;
            for (i = 0; i < tableData.length; i++) {
                displayBody +=  '<tr>' + '<td>' + tableData[i][0] + '</td>' +
                                '<td>' + tableData[i][1] + '</td>' +
                                '<td>' + tableData[i][2] + '</td>' + '</tr>';
            }
            displayBody += '</table>';

            let columnChartHTML = document.getElementById('column-chart-text');
            if (columnChartHTML) {
                columnChartHTML.innerHTML = displayBody;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
    }
}