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
            return search(input, "none", 1, 1, False, True, False)
        if select == "teams":
            return search(input, "none", 1, 1, True, False, False)
        else:
            return search(input, "none", 1, 1, False, False, True)
    else:
        team_list = database.getRelatedTerms('team')
        player_list = database.getRelatedTerms('player')
        game_list = database.getRelatedTerms('game')
        news_list = database.getAllNews()
        return render_template('index.html', team_list=team_list, player_list=player_list, game_list=game_list, news_list = news_list)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/players-<page_number>-<sr>-<query>-<filter>', methods=['POST', 'GET'])
def players(page_number, sr, query, filter):
    if request.method == 'POST':
        sort = int(request.form['sort'])
        if sort == 1:
            sort = int(sr)
        input = request.form['content']
        if input == "":
            input = query
        select = request.form['filter']
        if select == "none":
            select = filter
        return search(input, select, 1, sort, False, True, False)
    elif sr or query or filter != "0":
        cur_page = int(page_number)
        query_list = database.getRelatedTerms('player')
        players = database.searchDatabase(query, filter, cur_page, int(sr), False, True, False)
        pages = int(players.pop(len(players) - 1)) / 24
        return render_template('player-model.html', players=players, pages=pages, cur_page=cur_page, word_list=query_list, sr=sr, query=query, filter=filter)
    else:
        players = database.getAllPlayers(int(page_number))
        pages = database.getAllPlayersPgCount()
        cur_page = int(page_number)
        query_list = database.getRelatedTerms('player')
        return render_template('player-model.html', players=players, pages = pages, cur_page = cur_page, word_list=query_list, sr = sr,query="0",filter="0")


@app.route('/teams-<page_number>-<sr>-<query>-<filter>', methods=['POST', 'GET'])
def teams(page_number, sr, query, filter):
    if request.method == 'POST':
        sort = int(request.form['sort'])
        if sort==1:
            sort = int(sr)
        input = request.form['content']
        if input=="":
            input = query
        return search(input, "none", 1, sort, True, False, False)
    elif sr or query or filter != "0":
        cur_page = int(page_number)
        query_list = database.getRelatedTerms('team')
        teams = database.searchDatabase(query, "none", cur_page, int(sr), True, False, False)
        pages = int(teams.pop(len(teams)-1))/24
        return render_template('team-model.html', teams=teams, pages = pages, cur_page = cur_page, word_list=query_list, sr = sr, query = query, filter="0")
    else:
        teams = database.getAllTeams(int(page_number))
        pages = database.getAllTeamsPgCount()
        cur_page = int(page_number)
        query_list = database.getRelatedTerms('team')
        return render_template('team-model.html', teams=teams, pages = pages, cur_page = cur_page, word_list=query_list, sr=sr, query="0", filter="0")


@app.route('/games-<page_number>-<sr>-<query>-<filter>', methods=['POST', 'GET'])
def games(page_number, sr, query, filter):
    if request.method == 'POST':
        sort = int(request.form['sort'])
        if sort == 1:
            sort = int(sr)
        input = request.form['content']
        if input=="":
            input = query
        return search(input, "none", 1, sort, False, False, True)
    elif sr or query or filter != "0":
        cur_page = int(page_number)
        query_list = database.getRelatedTerms('game')
        games = database.searchDatabase(query, "none", cur_page, int(sr), False, False, True)
        pages = int(games.pop(len(games)-1))/24
        return render_template('game-model.html', games=games, pages = pages, cur_page = cur_page, word_list=query_list, sr = sr, query = query, filter="0")
    else:
        games = database.getAllGames(int(page_number))
        pages = database.getAllGamesPgCount()
        cur_page = int(page_number)
        query_list = database.getRelatedTerms('game')
        return render_template('game-model.html', games=games, pages = pages, cur_page = cur_page, word_list=query_list, sr=sr, query="0", filter="0")


@app.route('/player-instance<id>')
def player1(id):
    player = database.getPlayer(id)
    team = database.searchDatabase(player['team'], "none", 1, 1, True, False, False)
    news = database.getRelatedNews(player['name'])
    return render_template('player-instance.html', player = player, stats = player['stats'], team=team[0])


@app.route('/team-instance<id>')
def team1(id):
    team = database.getTeam(id)
    news = database.getRelatedNews(team['name'])
    return render_template('team-instance.html', team=team, news_list=news)


@app.route('/game-instance<id>')
def game1(id):
    game = database.getGame(id)
    home_id = game['home_id']
    away_id = game['away_id']
    home = database.getTeam(home_id)
    away = database.getTeam(away_id)
    return render_template('game-instance.html', home=home, away=away, game=game)


@app.route('/search-results')
def search(search, filter, page, sort, team, player, game):
        if search == "" and filter == "none" and sort == 1:
            if player == True:
                return redirect('/players-1-0-0-0')
            if team == True:
                return redirect('/teams1-0-0-0-0')
            if game == True:
                return redirect('/games1-0-0-0-0')
        results = database.searchDatabase(search, filter, page, sort, team, player, game)
        pages = results.pop(len(results)-1)/24
        if search == "":
            search = "0"
        if player == True:
            query_list = database.getRelatedTerms('player')
            return render_template('player-model.html', players=results, pages = pages, cur_page = 1, word_list=query_list, sr = str(sort), query = search, filter=filter)
        if team == True:
            query_list = database.getRelatedTerms('team')
            return render_template('team-model.html', teams=results, pages=pages, cur_page=1, word_list=query_list, sr=str(sort), query=search, filter = "0")
        if game == True:
            query_list = database.getRelatedTerms('game')
            return render_template('game-model.html', games=results, pages=pages, cur_page=1, word_list=query_list, sr=str(sort), query=search, filter="0")



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