from ncaam_bb_api import Player, Team, Game
from pymongo import MongoClient
from pprint import pprint
import re

# Read only access to database, no writing allowed
# Loads online database and its collections
client = MongoClient("mongodb+srv://college-basketball-infosite:YQYk9tu9KWZVckXU@cluster0.vkgny.gcp.mongodb.net/basketballdb?retryWrites=true&w=majority")
db = client['basketballdb']
teamCollection = db['Teams']
playerCollection = db['Players']
gameCollection = db['Games']


'''
Populates the online mongoDB database
Online database is currently up to date (and is read only), 
so this method won't add any new entries
'''
def setupDB():
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


'''
Returns a dictionary of the Team if database has the teamId, None otherwise
'''
def getTeam(teamId):
    team = None
    for t in teamCollection.find({'_id': str(teamId)}).limit(1):
        team = t
    return team


'''
Returns a dictionary of the Player if database has the teamId, None otherwise
'''
def getPlayer(playerId):
    player = None
    for p in playerCollection.find({'_id': str(playerId)}).limit(1):
        player = p
    return player


'''
Returns a dictionary of the Game if database has the teamId, None otherwise
'''
def getGame(gameId):
    game = None
    for g in playerCollection.find({'_id': str(gameId)}).limit(1):
        game = g
    return game


'''
Returns a list of all Team dictionaries in database
'''
def getAllTeams():
    teamList = []
    for t in teamCollection.find():
        teamList.append(t)
    return teamList


'''
Returns a list of all Player dictionaries in database
'''
def getAllPlayers():
    playerList = []
    for p in playerCollection.find():
        playerList.append(p)
    return playerList


'''
Returns a list of all Games dictionaries in database
'''
def getAllGames():
    gameList = []
    for g in gameCollection.find():
        gameList.append(g)
    return gameList


'''
Returns a list of all entries in the database that contains the query
Default search goes through all collections in database
'''
def searchDatabase(query, searchTeam = True, searchPlayer = True, searchGame = True):
    matches = []

    if searchTeam:
        for t in teamCollection.find():
            for value in t.values():
                if re.search(query, str(value)):
                    matches.append(t)
                    break
    
    if searchPlayer:
        for p in playerCollection.find():
            for value in p.values():
                if re.search(query, str(value)):
                    matches.append(p)
                    break
    
    if searchGame:
        for g in gameCollection.find():
            for value in g.values():
                if re.search(query, str(value)):
                    matches.append(g)
                    break

    return matches


'''
Updates the database with new fields, or new values to exisiting fields
Online database is up to date and read only, so don't call this method
'''
def updateDB():
    for t in teamCollection.find():
        team = Team(t['_id'])
        teamData = {}
        gameCollection.find_one_and_update({'_id': t['_id']}, {'$set': teamData})
        
    for g in gameCollection.find():
        game = Game(g['_id'], g['date'])
        
        gameData = {
            # 'thumbnail': game.thumbnail,
            # 'highlights': game.highlights
        }
        gameCollection.find_one_and_update({'_id': g['_id']}, {'$set': gameData})

    for p in playerCollection.find():
        player = Player(p['_id'])
        playerData = {
            # 'headshot': player.headshot
        }
        playerCollection.find_one_and_update({'_id': p['_id']}, {'$set': playerData})