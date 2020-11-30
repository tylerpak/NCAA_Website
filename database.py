import string

from ncaam_bb_api import Player, Team, Game, News
from pymongo import MongoClient
from pprint import pprint
import re
import youtube_search

# Read only access to database, no writing allowed
# Loads online database and its collections
__client = MongoClient("mongodb+srv://college-basketball-infosite:YQYk9tu9KWZVckXU@cluster0.vkgny.gcp.mongodb.net/basketballdb?retryWrites=true&w=majority")
__db = __client['basketballdb']
teamCollection = __db['Teams']
playerCollection = __db['Players']
gameCollection = __db['Games']
newsCollection = __db['News']
autocompleteCollection = __db['Autocomplete']

class Database:
    __instance = None

    def __init__(self):
        Database.__instance = self
        
    def getInstance():
        if Database.__instance == None:
            Database()
        return Database.__instance

    '''
    Populates the online mongoDB database
    Online database is currently up to date (and is read only), 
    so this method won't add any new entries
    '''
    def setupDB(self):
        teamList = Team.populate()
        for t in teamList:
            in_db = teamCollection.count_documents({'_id': teamList.get(t)})
            teamData = None

            if in_db == 0: # if not in db, get info from API and add to db
                team = Team(teamList.get(t))
                teamData = {
                    '_id': team.team_id, 
                    'name': team.name, 
                    'record': team.record, 
                    'logo': team.logo, 
                    'roster_link': team.roster_link, 
                    'roster': team.roster,
                    'schedule_link': team.schedule_link,
                    'schedule': team.schedule,
                    'links': team.links}
                teamCollection.insert_one(teamData)

            else: # else find team in database
                for article in teamCollection.find({'_id': teamList.get(t)}).limit(1):
                    teamData = article

            scheduleDict = teamData['schedule']
            for gameId in scheduleDict:
                date = scheduleDict[gameId][0]

                if gameCollection.count_documents({'_id': gameId}) == 0: # if game not in db, add it to db
                    game = Game(gameId, date)
                    gameData = {
                        '_id': game.game_id,
                        'date': game.date,
                        'home_id': game.home_id,
                        'away_id': game.away_id,
                        'home_name': game.home_name,
                        'away_name': game.away_name,
                        'name': game.name,
                        'venue': game.venue,
                        'links': game.links,
                        'thumbnail': game.thumbnail,
                        'highlights': game.highlights
                    }
                    gameCollection.insert_one(gameData)

            playerIdList = teamData['roster'][1]
            for p in playerIdList:
                in_db = playerCollection.count_documents({'_id': p})

                if in_db == 0: #if player not in db, add to db
                    player = Player(p)
                    playerData = {
                        '_id': player.player_id,
                        'name': player.name,
                        'birthplace': player.birthplace,
                        'height': player.height,
                        'jersey': player.jersey,
                        'links': player.links,
                        'position': player.position,
                        'stats': player.stats,
                        'team': player.team,
                        'weight': player.weight,
                        'headshot': player.headshot
                    }
                    playerCollection.insert_one(playerData)
        
        news = News()

        for a in news.articles:
            newsData = {
                'headline': a['headline'],
                'description': a['description'],
                'images': a['images']
            }
            newsCollection.insert(newsData)


    '''
    Returns a dictionary of the Team if database has the teamId, None otherwise
    '''
    def getTeam(self, teamId):
        team = None
        for t in teamCollection.find({'_id': str(teamId)}).limit(1):
            team = t
        return team


    '''
    Returns a dictionary of the Player if database has the teamId, None otherwise
    '''
    def getPlayer(self, playerId):
        player = None
        for p in playerCollection.find({'_id': str(playerId)}).limit(1):
            player = p
        return player


    '''
    Returns a dictionary of the Game if database has the teamId, None otherwise
    '''
    def getGame(self, gameId):
        game = None
        for g in gameCollection.find({'_id': str(gameId)}).limit(1):
            game = g
        return game


    '''
    Finds all news that contains the keyword in the headline or description
    '''
    def getRelatedNews(self, keyword):
        newsList = []
        splitWords = keyword.split()

        for n in newsCollection.find():
            for word in splitWords:
                if re.search(word, n['description']) or re.search(word, n['headline']):
                    newsList.append(n)
                    break
        
        return newsList


    '''
    Returns a list of all Team dictionaries in database
    '''
    def getAllTeams(self, page_number):
        teamList = []
        for t in teamCollection.find().skip(24 * (page_number - 1)).limit(24):
            teamList.append(t)
        return teamList


    '''
    Returns number of pages necessary for teams 
    '''
    def getAllTeamsPgCount(self):
        return teamCollection.count() / 24


    '''
    Returns a list of all Player dictionaries in database
    '''
    def getAllPlayers(self, page_number):
        playerList = []
        for p in playerCollection.find().skip(24*(page_number-1)).limit(24):
            playerList.append(p)
        return playerList

    '''
    Returns number of pages necessary for players 
    '''
    def getAllPlayersPgCount(self):
        return playerCollection.count() / 24

    '''
    Returns a list of all Games dictionaries in database
    '''
    def getAllGames(sefl, page_number):
        gameList = []
        for g in gameCollection.find().skip(24 * (page_number - 1)).limit(24):
            gameList.append(g)
        return gameList

    '''
    Returns number of pages necessary for teams 
    '''
    def getAllGamesPgCount(self):
        return gameCollection.count() / 24


    '''
    Get all news articles in database
    '''
    def getAllNews(self):
        articles = []
        for a in newsCollection.find():
            articles.append(a)
        
        return articles

    '''
    Sort player results
    '''
    def sortPlayers(self, sort, players):
        if sort == 2:
            players.sort(key=lambda x: x['name'])
        elif sort == 3:
            players.sort(key=lambda x: x['name'], reverse=True)
        elif sort == 4:
            players.reverse()
        elif sort == 5:
            players.sort(key=lambda x: x['weight'])
        elif sort == 6:
            players.sort(key=lambda x: x['weight'], reverse=True)
        else:
            return players
        return players


    '''
    Sort team results
    '''
    def sortTeams(self, sort, teams):
        if sort == 2:
            teams.sort(key=lambda x: x['name'])
        elif sort == 3:
            teams.sort(key=lambda x: x['name'], reverse=True)
        else:
            return teams
        return teams


    '''
    Sort game results
    '''
    def sortGames(self, sort, games):
        if sort == 2:
            games.sort(key=lambda x: x['home_name'])
        elif sort == 3:
            games.sort(key=lambda x: x['home_name'], reverse=True)
        elif sort == 4:
            games.sort(key=lambda x: x['away_name'])
        elif sort == 5:
            games.sort(key=lambda x: x['away_name'], reverse=True)
        elif sort == 6:
            games.sort(key=lambda x: x['venue'])
        elif sort ==7:
            games.sort(key=lambda x: x['venue'], reverse=True)
        else:
            return games
        return games


    '''
    Returns a list of all entries in the database that contains the query
    Default search goes through all collections in database
    '''
    def searchDatabase(self, query, filter, page_number, sort, searchTeam = True, searchPlayer = True, searchGame = True,):
        matches = []

        if searchTeam:
            for t in teamCollection.find():
                for value in t.values():
                    if re.search(query.lower(), str(value).lower()):
                        matches.append(t)
                        break
        
        if searchPlayer:
            for p in playerCollection.find():
                flag1 = False
                if filter == "none":
                    flag2 = True
                else:
                    flag2 = False
                for value in p.values():
                    if re.search(filter, str(value).lower()):
                        flag2 = True
                    if re.search(query.lower(), str(value).lower()):
                        flag1 = True
                    if flag1 and flag2 is True:
                        matches.append(p)
                        break

        if searchGame:
            for g in gameCollection.find():
                for value in g.values():
                    if re.search(query.lower(), str(value).lower()):
                        matches.append(g)
                        break

        if searchPlayer:
            matches = sortPlayers(sort, matches)
        if searchTeam:
            matches = sortTeams(sort, matches)
        if searchGame:
            matches = sortGames(sort, matches)

        output = matches[(24*(page_number-1)):]
        output = output[:24]
        output.append(len(matches))
        return output

    '''
    Gets all words related to the model (team, player, or games) for autocomplete
    Used to store in database, don't use in app.py (look at getRelatedTerms())
    '''
    def autocomplete(self, model):
        matches = []
        if re.match('team', model):
            for t in teamCollection.find():
                matches.append(t['name'])
                for player in t['roster'][0]:
                    matches.append(player)

        if re.match('player', model):
            for p in playerCollection.find():
                if p['name'] not in matches:
                    matches.append(p['name'])
                if p['team'] not in matches:
                    matches.append(p['team'])
                if p['position'] not in matches:
                    matches.append(p['position'])

        if re.match('game', model):
            for g in gameCollection.find():
                if g['name'] not in matches:
                    matches.append(g['name'])
                if g['home_name'] not in matches:
                    matches.append(g['home_name'])
                if g['away_name'] not in matches:
                    matches.append(g['away_name'])
                if g['venue'] not in matches:
                    matches.append(g['venue'])

        matches.sort()
        return matches


    '''
    Gets all the related terms to model (team, player, game) from the database
    Returns an empty list if model is not found
    '''
    def getRelatedTerms(self, model):
        matches = []

        for related in autocompleteCollection.find({'_id': model}):
            return related['related_terms']

        return matches


    '''
    Updates the database with new fields, or new values to exisiting fields
    Online database is up to date and read only, so don't call this method
    '''
    def updateDB(self):
        return 0
