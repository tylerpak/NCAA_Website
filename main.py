from flask import Flask, render_template

app = Flask(__name__)


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
    app.run(debug=True)