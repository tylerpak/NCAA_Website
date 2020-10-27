from flask import Flask, render_template
from pprint import pprint
import database

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/players<page_number>')
def players(page_number):
    players = database.getAllPlayers(int(page_number))
    pages = database.getAllPlayersPgCount()
    cur_page = int(page_number)
    if cur_page < 2:
        cur_page = 2
    if cur_page == pages:
        cur_page = cur_page - 1
    return render_template('player-model.html', players=players, pages = pages, cur_page = cur_page)

@app.route('/teams<page_number>')
def teams(page_number):
    teams = database.getAllTeams(int(page_number))
    pages = database.getAllTeamsPgCount()
    cur_page = int(page_number)
    if cur_page < 2:
        cur_page = 2
    if cur_page == pages:
        cur_page = cur_page - 1
    return render_template('team-model.html', teams=teams, pages = pages, cur_page = cur_page)

@app.route('/games<page_number>')
def games(page_number):
    games = database.getAllGames(int(page_number))
    pages = database.getAllGamesPgCount()
    cur_page = int(page_number)
    if cur_page < 2:
        cur_page = 2
    if cur_page == pages:
        cur_page = cur_page - 1
    return render_template('game-model.html', games=games, pages = pages, cur_page = cur_page)

@app.route('/player-instance<id>')
def player1(id):
    player = database.getPlayer(id)
    return render_template('player-instance.html', player = player, stats = player['stats'])


@app.route('/team-instance<id>')
def team1(id):
    team = database.getTeam(id)
    return render_template('team-instance.html', team=team)



@app.route('/game-instance<id>')
def game1(id):
    game = database.getGame(id)
    home_id = game['home_id']
    away_id = game['away_id']
    home = database.getTeam(home_id)
    away = database.getTeam(away_id)
    return render_template('game-instance.html', home=home, away=away, game=game)




if __name__ == "__main__":
    app.run(debug=True)