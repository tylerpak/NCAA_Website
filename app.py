import math
from flask import Flask, render_template, request, redirect, flash
from pprint import pprint

import database


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        input = request.form['content']
        select = request.form['filter']
        if select == "players":
            return search(input, False, True, False)
        if select == "teams":
            return search(input, True, False, False)
        else:
            return search(input, False, False, True)
    else:
        return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/players<page_number>', methods=['POST', 'GET'])
def players(page_number):
    if request.method == 'POST':
        input = request.form['content']
        return search(input, False, True, False)
    else:
        players = database.getAllPlayers(int(page_number))
        pages = database.getAllPlayersPgCount()
        cur_page = int(page_number)
        query_list = database.autocomplete('player')
        return render_template('player-model.html', players=players, pages = pages, cur_page = cur_page, word_list=query_list)


@app.route('/teams<page_number>', methods=['POST', 'GET'])
def teams(page_number):
    if request.method == 'POST':
        input = request.form['content']
        return search(input, True, False, False)
    else:
        teams = database.getAllTeams(int(page_number))
        pages = database.getAllTeamsPgCount()
        cur_page = int(page_number)
        query_list = database.autocomplete('team')
        return render_template('team-model.html', teams=teams, pages = pages, cur_page = cur_page, word_list=query_list)


@app.route('/games<page_number>', methods=['POST', 'GET'])
def games(page_number):
    if request.method == 'POST':
        input = request.form['content']
        return search(input, False, False, True)
    else:
        games = database.getAllGames(int(page_number))
        pages = database.getAllGamesPgCount()
        cur_page = int(page_number)
        query_list = database.autocomplete('game')
        return render_template('game-model.html', games=games, pages = pages, cur_page = cur_page, word_list=query_list)


@app.route('/player-instance<id>')
def player1(id):
    player = database.getPlayer(id)
    team = database.searchDatabase(player['team'], True, False, False)
    news = database.getRelatedNews(player['name'])
    return render_template('player-instance.html', player = player, stats = player['stats'], team=team[0])


@app.route('/team-instance<id>')
def team1(id):
    team = database.getTeam(id)
    news = database.getRelatedNews(team['name'])
    return render_template('team-instance.html', team=team)


@app.route('/game-instance<id>')
def game1(id):
    game = database.getGame(id)
    home_id = game['home_id']
    away_id = game['away_id']
    home = database.getTeam(home_id)
    away = database.getTeam(away_id)
    return render_template('game-instance.html', home=home, away=away, game=game)


@app.route('/search-results')
def search(search, team, player, game):
        results = database.searchDatabase(search, team, player, game)
        pages = 1
        if search == "":
            if player == True:
                return redirect('/players1')
            if team == True:
                return redirect('/teams1')
            if game == True:
                return redirect('/games1')
        if len(results) != 0:
            pages = len(results)/24
        if player == True:
            query_list = database.autocomplete('player')
            return render_template('player-model.html', players=results, pages = pages, cur_page = 1, word_list=query_list)
        if team == True:
            query_list = database.autocomplete('team')
            return render_template('team-model.html', teams=results, pages=pages, cur_page=1, word_list=query_list)
        if game == True:
            query_list = database.autocomplete('game')
            return render_template('game-model.html', games=results, pages=pages, cur_page=1, word_list=query_list)



@app.context_processor
def utility_processor():
    def game_exists(id):
        return database.getGame(id)
    return dict(game_exists=game_exists)

@app.context_processor
def utility_processor2():
    def get_gameName(id):
        game = database.getGame(id)
        name = game['home_name'] + ' vs ' + game['away_name']
        return name
    return dict(get_gameName=get_gameName)

@app.context_processor
def utility_processor3():
    def player_exists(id):
        return database.getPlayer(id)
    return dict(player_exists=player_exists)



if __name__ == "__main__":
    app.run(debug=True)