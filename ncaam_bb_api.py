import requests
import json
import time
import re

sportsio_url = "https://api.sportsdata.io/v3/cbb/scores/json/"
api_key = "ee65f6fe551f4fe98d0b63c5c96b2279"

espn_url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/"

#response = requests.get(sportsio_url+call, headers={"Ocp-Apim-Subscription-Key": api_key})

def collect_json(url, filename):
	response = requests.get(url)
	data = response.json()

	with open(filename, 'w') as json_file:
		json.dump(data, json_file)

def change_date(input, year):
	months = {"nov": "11", "dec": "12", "jan": "01", "feb": "02", "mar": "03", "apr": "04"}
	in_month = re.search(r""", [a-z]{3}""", input.lower()).group()[2:]
	in_month = months[in_month]
	in_day = re.search(r"""(?:\d\d|\d)""", input).group()
	if len(in_day) == 1:
		in_day = "0"+in_day
	return year+in_month+in_day


'''
Attributes:
	-response
	-roster
		-list of Player()
	-schedule
		-list of Game()
	-name
	-logo
	-record
	-links
'''
class Team:
	url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/"

	def __init__(self, team_id, *args):
		self.team_id = str(team_id)
		response = requests.get(self.url+self.team_id).json()
		if response["team"]["isActive"] == False:
			self.logo = "https://cdn0.iconfinder.com/data/icons/files-49/32/tn12_file_broken_warning_error_mistake_document_interface_-512.png"
		else:
			self.logo = response["team"]["logos"][0]["href"]

		self.roster_link = response["team"]["links"][1]["href"]
		self.roster = self.get_team_roster()
		self.schedule_link = response["team"]["links"][3]["href"]
		self.schedule = self.get_team_schedule()
		self.name = response["team"]["displayName"]
		self.record = response["team"]["record"]
		link = response["team"]["links"]
		self.links = {}
		for x in link:
			self.links[x["shortText"]] = [x["href"]]
		#self.links = {link[0]["shortText"]: link[0]["href"], link[1]["shortText"]: link[1]["href"], link[2]["shortText"]: link[2]["href"], link[3]["shortText"]: link[3]["href"], link[4]["shortText"]: link[4]["href"], link[5]["shortText"]: link[5]["href"]}

		if args:
			if args[0] == True:
				self.roster = self.get_team_roster()
		if len(args) == 2:
			if args[1] == True:
				self.schedule = self.get_team_schedule()

	def __str__(self):
		return self.name

	'''
	get_team_roster takes a link and returns a list of player names
	'''
	def get_team_roster(self):
		response = requests.get(self.roster_link)
		raw_html = response.content
		desired_lines = re.findall(r"""<a class="AnchorLink" tabindex="0" href="http://www\.espn\.com/mens-college-basketball/player/_/id/[0-9]*/[a-z-]*">[a-z A-Z .]*</a>""", str(raw_html))
		names = []
		ids = []
		players = []
		
		for a in desired_lines:
			names.append(re.search('>[a-z A-Z .]*<', a).group()[1:-1])
			ids.append(re.search('id/[0-9]*/', a).group()[3:-1])
			#players.append(Player(ids[-1]))
		
		return [names, ids]

	'''
	get_team_schedule takes a team's schedule url and returns a dictionary with basic info and Game instances
	'''
	def get_team_schedule(self):
		url = "https://www.espn.com/mens-college-basketball/team/schedule/_/id/" + str(self.team_id) + "/season/2019"
		response = requests.get(url)
		raw_html = response.content
		date_lines = re.findall(r"""<td class="Table__TD"><span>[a-zA-Z]{3}, [a-zA-Z]{3} \d+</span></td><td class="Table__TD"><div class="flex items-center opponent-logo"><span class="pr2">(?:vs|@)</span><span class="tc pr2" style="width:20px;height:20px"><a""", str(raw_html))
		opponent_lines = re.findall(r"""<a class="AnchorLink" tabindex="0" href="/mens-college-basketball/team/_/id/[0-9]*/[a-z-]*">[a-zA-Z 0-9 \&\#\; ']*<!-- --> </a>""", str(raw_html))
		id_lines = re.findall(r"""<a class="AnchorLink" tabindex="0" href="http://www\.espn\.com/mens-college-basketball/game\?gameId=[0-9]*">(?:\d\d\d|\d\d)-(?:\d\d\d|\d\d) (?:|OT)<!-- --> </a>""", str(raw_html))
		opponents = []
		results = []
		opp_ids = []
		game_ids = []
		dates = []

		for a in opponent_lines:
			a = a.replace("amp;", '')
			a = a.replace("&#x27;", "'")
			opponents.append(re.search(r""">[a-zA-Z 0-9 \&\#\; ']*<""", a).group()[1:-1])
			opp_ids.append(re.search(r"""id/[0-9]*/""", a).group()[3:-1])

		for a in date_lines:
			a = a[0:-155]
			dates.append(re.search(r""">[a-zA-Z]{3}, [a-zA-Z]{3} \d+<""", a).group()[1:-1])

		for a in id_lines:
			game_ids.append(re.search(r'''Id=[0-9]*"''', a).group()[3:-1])
			results.append(re.search(r"""(?:\d\d\d|\d\d)-(?:\d\d\d|\d\d)""", a).group())

		i = 0
		schedule = {}
		while(i < len(date_lines)):
			#game = Game(game_ids[i], change_date(dates[i], url[-4:]))
			schedule[game_ids[i]] = [dates[i], opponents[i], results[i], opp_ids[i]]
			i += 1
		
		return schedule


	'''
	populate returns a dict of keys team name with value team id for all teams in D1
	'''
	def populate():
		url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams?region=us&lang=en&contentorigin=espn&limit=900"
		response = requests.get(url).json()
		teams_list = response["sports"][0]["leagues"][0]["teams"]
		teams = {}

		for team in teams_list:
			teams[team["team"]["displayName"]] = team["team"]["id"]
			#teams.append(Team(team["team"]["id"]))


		return teams

'''
Attributes:
	-response
	-name
	-team/school
	-position
	-year
	-jersey
	-birthplace
	-height
	-weight
	-stats
		-points
		-assists
		-rebounds
	-links
'''
class Player:
	url = "https://site.web.api.espn.com/apis/common/v3/sports/basketball/mens-college-basketball/athletes/"

	def __init__(self, player_id):
		self.player_id = str(player_id)
		response = requests.get(self.url+self.player_id).json()
		self.name = response["athlete"]["displayName"]
		self.team = response["athlete"]["team"]["displayName"]
		self.position = response["athlete"]["position"]["displayName"]
		self.year = response["athlete"]["displayExperience"]
		self.jersey = response["athlete"]["displayJersey"]
		self.birthplace = response["athlete"]["displayBirthPlace"]
		self.height = response["athlete"]["displayHeight"]
		self.weight = response["athlete"]["displayWeight"]
		link = response["athlete"]["links"]
		self.links = {}
		for x in link:
			self.links[x["shortText"]] = [x["href"]]

		try:
			statline = response["athlete"]["statsSummary"]["statistics"]
			#self.stats = {statline[0]["shortDisplayName"]: statline[0]["displayValue"], statline[1]["shortDisplayName"]: statline[1]["displayValue"], statline[2]["shortDisplayName"]: statline[2]["displayValue"], statline[3]["shortDisplayName"]: statline[3]["displayValue"]}
			self.stats = statline[0:4]
		except:
			self.stats = {}

	def __str__(self):
		return self.name

	def populate():
		return

'''
Attributes:
	-name
	-score
	-home team
	-away team
	-date
	-venue
	-stats
	-links
'''
class Game:
	url = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?lang=en&region=us&limit=500&dates="

	def __init__(self, game_id, date):
		self.game_id = str(game_id)
		self.date = str(date)
		response = requests.get(self.url+self.date+"&groups=50").json()
		
		for x in response["events"]:
			if x["id"] == self.game_id:
				game = x
		
		self.home_id = game["competitions"][0]["competitors"][0]["id"]
		self.away_id = game["competitions"][0]["competitors"][1]["id"]
		self.home_name = game["competitions"][0]["competitors"][0]["team"]["displayName"]
		self.away_name = game["competitions"][0]["competitors"][1]["team"]["displayName"]
		#self.date = game["date"]
		self.name = game["name"]
		self.venue = game["competitions"][0]["venue"]["fullName"]
		link = game["links"]
		self.links = {}
		for x in link:
			self.links[x["shortText"]] = [x["href"]]

	def __str__(self):
		return(self.name)

	def populate():
		return

#Games by date
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard?lang=en&region=us&limit=500&dates={date yyyymmdd}}&groups=50

#Games today
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard

#Current news
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/news

#Team by ID
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams/{team ID}

#Teams list
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/teams?region=us&lang=en&contentorigin=espn&limit=900

#Groups->leagues->teams->rosters
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/groups

#Athlete by ID
#https://site.web.api.espn.com/apis/common/v3/sports/basketball/mens-college-basketball/athletes/{athlete ID}

#Current Rankings
#https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/rankings

#Roster ID example
#http://www.espn.com/mens-college-basketball/team/roster/_/id/251

#Team schedule by ID and season year. NOT API
#https://www.espn.com/mens-college-basketball/team/schedule/_/id/{team ID}/season/{yyyy}

#<a class="AnchorLink" tabindex="0" href="http://www.espn.com/mens-college-basketball/game?gameId=401166411">69-45  </a>
#<a class="AnchorLink" tabindex="0" href="/mens-college-basketball/team/_/id/2458/northern-colorado-bears">Northern Colorado<!-- --> </a>
#<a class="AnchorLink" tabindex="0" href="/mens-college-basketball/team/_/id/2608/saint-marys-gaels">Saint Mary's<!-- --> </a>
#<td class="Table__TD"><span>Sat, Nov 9</span></td><td class="Table__TD"><div class="flex items-center opponent-logo"><span class="pr2">vs</span><span class="tc pr2" style="width:20px;height:20px"><a
#<a class="AnchorLink" tabindex="0" href="http://www.espn.com/mens-college-basketball/game?gameId=401171584">76-58 <!-- --> </a>