// Show/hide the drop down list of autocomplete suggesetions for model pages
function find_related(input){
    var text_input = document.getElementById('content');
    if (input == ""){
        text_input.setAttribute('list', null);
    }
    else{
        text_input.setAttribute('list', 'datalist');
    }
}

// Changes the autocomplete lists for the main search bar (for filtering)
function changelist(){
    var filter = document.getElementById('filter').value;
    var text_input = document.getElementById('content');
    if (text_input.value == ""){
      text_input.setAttribute('list', null);
    }
    else if (filter == "players"){
      text_input.setAttribute('list', 'player-list');
    }
    else if (filter == "teams"){
      text_input.setAttribute('list', 'team-list');
    }
    else if (filter == "games"){
      text_input.setAttribute('list', 'game-list');
    }
}