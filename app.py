from flask import Flask, render_template
from ncaam_bb_api import Player, Team, Game
import pymongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient()
db = client['cbidb']

teamsDictionary = Team.populate()
articles = db.articles
# result = articles.insert(teamsDictionary)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    # print(articles.count())

    app.run(debug=True)