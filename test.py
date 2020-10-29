import ncaam_bb_api as ncaa
import unittest

class Test_ESPN_API(unittest.TestCase):

	def test_team_init(self):
		team_id_list = [2000, 2005, 2006, 38, 171]

		for x in team_id_list:
			temp = ncaa.Team(x)
			print(temp.name)

			#Roster
			self.assertIsInstance(temp.roster[0], list)
			self.assertIsInstance(temp.roster[1], list)

			#Schedule
			self.assertIsInstance(temp.schedule, dict)
			
			#Name
			self.assertIsInstance(temp.name, str)

			#Record
			self.assertIsInstance(temp.record, dict)

			#Links
			self.assertIsInstance(temp.links, dict)

	def test_player_init(self):
		player_id_list = ['4431691', '4277918', '4397079', '4277921', '4277920', '4397080', '4066325', '4431699', '4397076', '4334018', '4277922', '4402811', '4592304']

		for x in player_id_list:
			temp = ncaa.Player(x)
			#Name
			self.assertIsInstance(temp.name, str)
			print(temp.name)

			#Headshot
			self.assertIsInstance(temp.headshot, str)

			#School
			self.assertIsInstance(temp.team, str)

			#Position
			self.assertIsInstance(temp.position, str)

			#Year
			self.assertIsInstance(temp.year, str)

			#Jersey
			self.assertIsInstance(temp.jersey, str)

			#Birthplace
			self.assertIsInstance(temp.birthplace, str)

			#Height
			self.assertIsInstance(temp.height, str)

			#Weight
			self.assertIsInstance(temp.weight, str)

			#Stats
			self.assertIsInstance(temp.stats, list)
			for y in temp.stats:
				self.assertIsInstance(y, dict)

			#Links
			self.assertIsInstance(temp.links, dict)
			for y in temp.links.keys():
				self.assertIsInstance(y, str)

			for y in temp.links.values():
				self.assertIsInstance(y, list)
				for z in y:
					self.assertIsInstance(z, str)

	def test_game_init(self):
		games = [['401166411', 'Tue, Nov 5'], ['401166030', 'Tue, Nov 12'], ['401169616', 'Fri, Nov 15'], ['401168386', 'Thu, Nov 21']]
		for game in games:
			temp = ncaa.Game(game[0], game[1])

			#Name
			self.assertIsInstance(temp.name, str)
			print(temp.name)

			#Score
			self.assertIsInstance(temp.score, str)
			print(temp.score)

			#Home Team
			self.assertIsInstance(temp.home_name, str)
			print(temp.home_name)

			#Away Team
			self.assertIsInstance(temp.away_name, str)
			print(temp.away_name)

			#Date
			self.assertIsInstance(temp.date, str)
			print(temp.date)

			#Venue
			self.assertIsInstance(temp.venue, str)
			print(temp.venue)

			#Links
			self.assertIsInstance(temp.links, dict)
			print(temp.links)

			#Thumbnail
			self.assertIsInstance(temp.thumbnail, str)
			print(temp.thumbnail)

			#Highlights
			self.assertIsInstance(temp.highlights, str)
			print(temp.highlights)
		return


if __name__ == "__main__":
	unittest.main()


'''x = ncaa.Team(251)
print(x.schedule)'''