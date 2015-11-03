#-*- coding: utf-8 -*-
import tournament
from datetime import datetime

#------------------------------------------------

class PlayerMatchLog:
	def __init__(self, opponent, rating, description):
		self.opponent = opponent
		self.rating = rating
		self.description = description

#------------------------------------------------

class PlayerTournamentLog:
	def __init__(self, tournamentName, tournamentDate):
		self.tournamentName = tournamentName
		self.tournamentDate = tournamentDate
		self.matchLogs = []

	def addMatch(self, opponent, rating, description):
		self.matchLogs.append(PlayerMatchLog(opponent, rating, description))

	def getLastRating(self):
		return self.matchLogs[-1].rating

#------------------------------------------------

class PlayerRating:
	def __init__(self, player, legend, basicRating):
		self.player = player
		self.legend = legend
		self.basicRating = basicRating
		self.tournamentLogs = []
		self.locations = dict()


	def addMatch(self, tournamentName, tournamentData, locations, opponent, rating, description):
		if not tournamentName in [x.tournamentName for x in self.tournamentLogs]:
			self.tournamentLogs.append(PlayerTournamentLog(tournamentName, tournamentData))
		pass
		pos = [x.tournamentName for x in self.tournamentLogs].index(tournamentName)
		self.tournamentLogs[pos].addMatch(opponent, rating, description)
		for city in locations:
			if city in self.locations:
				if self.locations[city] < tournamentData:
					self.locations[city] = tournamentData
			else:
				self.locations[city] = tournamentData
			pass

	def saveHistory(self, filePath):
		historyStr = self.legend + "\n"
		for tournament in self.tournamentLogs:
			historyStr += tournament.tournamentName + "\n"
			for match in tournament.matchLogs:
				historyStr += match.description + "\n"
		file = open(filePath, 'w', encoding='utf8')
		file.write(historyStr)

	def getLastRating(self):
		if len(self.tournamentLogs) == 0:
			return self.basicRating
		return self.tournamentLogs[-1].getLastRating()

	def getRatingAfterTime(self, time):
		pos = -1
		for i in range(len(self.tournamentLogs)):
			if self.tournamentLogs[i].tournamentDate < time:
				pos = i
			else:
				break
		if pos == -1:
			return self.basicRating
		return self.tournamentLogs[pos].getLastRating()

#------------------------------------------------

if __name__ == "__main__":
	pass
	playerRating = PlayerRating("Blah Blah", "legend")
	tournament = tournament.Tournament("tournament_logs/2014-07-05_msk_regional.ant")
	playerRating.addMatch(tournament, "Enemy", 20, "Some shit")
	pass