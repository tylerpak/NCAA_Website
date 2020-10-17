from flask import Flask, render_template
from ncaam_bb_api import Player, Team, Game
from pymongo import MongoClient
from pprint import pprint


# password ='YQYk9tu9KWZVckXU'
# mongodb_url = 'mongodb+srv://college-basketball-infosite:YQYk9tu9KWZVckXU@cluster0.vkgny.gcp.mongodb.net/basketballdb?retryWrites=true&w=majority'
app = Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://college-basketball-infosite:YQYk9tu9KWZVckXU@cluster0.vkgny.gcp.mongodb.net/basketballdb?retryWrites=true&w=majority")
db = client['basketballdb']

teamCollection = db['Teams']
playerCollection = db['Players']
gameCollection = db['Games']

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


def setupDB():
    teamList = Team.populate()
    for t in teamList:
        in_db = teamCollection.count_documents({'name': t})
        teamData = None

        if in_db == 0: # if not in db, get info from API and add to db
            team = Team(teamList.get(t))
            teamData = {'_id': team.team_id, 
                'name': team.name, 
                'record': team.record, 
                'logo': team.logo, 
                'roster_link': team.roster_link, 
                'roster': team.roster,
                'links': team.links}
            teamCollection.insert_one(teamData)

        else: # else find team in database
            for article in teamCollection.find({'name': t}).limit(1):
                teamData = article
            # pprint(teamData)

if __name__ == "__main__":
    setupDB()
    app.run(debug=True)