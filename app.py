from flask import Flask, render_template
from ncaam_bb_api import Player, Team, Game
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient()
db = client['basketballdb']

# db.create_collection('Players')
# db.create_collection('Teams')
# db.create_collection('Games')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/players')
def players():
    return render_template('player-model.html')

@app.route('/teams')
def teams():
    return render_template('team-model.html')

@app.route('/games')
def games():
    return render_template('game-model.html')

@app.route('/royce-hamm')
def player1():
    return render_template('royce-hamm.html')

@app.route('/jalen-hill')
def player2():
    return render_template('jalen-hill.html')

@app.route('/taz-sherman')
def player3():
    return render_template('taz-sherman.html')

@app.route('/longhorns')
def team1():
    return render_template('longhorns.html')


@app.route('/mountaineers')
def team2():
    return render_template('mountaineers.html')


@app.route('/sooners')
def team3():
    return render_template('sooners.html')


@app.route('/game1')
def game1():
    return render_template('game1.html')


@app.route('/game2')
def game2():
    return render_template('game2.html')


@app.route('/game3')
def game3():
    return render_template('game3.html')


if __name__ == "__main__":
    # db.get_collection('Teams').drop()

    teamList = Team.populate()
    for t in teamList:

        if db.get_collection('Team').find_one({'_id': str(teamList.get(t))}) == False: #if not in database, get from API
            print('added new team: {}'.format(t))
            team = Team(teamList.get(t))
            teamData = {'_id': team.team_id, 
                'name': team.name, 
                'record': team.record, 
                'logo': team.logo, 
                'roster_link': team.roster_link, 
                'roster': team.roster, 
                'links': team.links}
            db.get_collection('Teams').insert_one(teamData)

        # roster = team.get_team_roster()
        # print(roster)
        # p = roster[1][0]
        # player = Player(p)
        # print(p)
        # if db.get_collection('Player').find_one(p) == False:
        #     playerMap = {'_id': player.player_id, 'name': player.name, 'position': player.position}
        #     db.get_collection('Players').insert_one(playerMap)
            # if db.get_collection('Players').find_one()

    # for article in db.get_collection('Teams').find():
        # print(article)

    # app.run(debug=True)