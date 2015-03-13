#-*- coding: utf-8 -*-
import xmltodict
import os
import collections
import copy
from datetime import datetime

# ----------------------------

class Match:
	def __init__(self, gameDict):
		self.playerA = gameDict["player1"]
		self.playerB = gameDict["player2"]
		self.prestigeA = int(gameDict["prestige1"])
		self.prestigeB = int(gameDict["prestige2"])
		self.gamesCount = int(gameDict["gamesCount"])

	def calculatePrestige(self):
		return (self.prestigeA, self.prestigeB)

	def calculateWins(self):
		totalPrestige = self.prestigeA + self.prestigeB
		coef = float(self.gamesCount)/float(totalPrestige)
		return (coef * self.prestigeA, coef * self.prestigeB)

	def toStringPlayerAPoints(self):
		return "(" + str(self.prestigeA) + ")"


	def toStringPlayerBPoints(self):
		return "(" + str(self.prestigeB) + ")"

	def toStringPlayerAMatch(self):
		return self.playerA + " " + self.toStringPlayerAPoints() + " - " + self.toStringPlayerBPoints() + " " + self.playerB

	def toStringPlayerBMatch(self):
		return self.playerB + " " + self.toStringPlayerBPoints() + " - " + self.toStringPlayerAPoints() + " " + self.playerA

	def getCountGames(self):
		return self.gamesCount

# ----------------------------

class Tournament:
	def __init__(self, filePath):
		self.name = filePath
		file = open(filePath, 'r', encoding='utf8')
		tournamentDict  = xmltodict.parse(file.read())
		tournamentDict = tournamentDict["root"]
		file.close()

		self.date = datetime.strptime(tournamentDict["header"]["date"][:13], '%Y-%m-%dT%H')  #2014-02-24T00:00:00+04:00
		print(self.date)

		self.matches = list()
		for game in tournamentDict["games"]["item"]:
			self.matches.append(Match(game))
			pass

		print("Done")

# -----------------------------------------------------------------

def retrivePlayers(matches):
	players = []
	for match in matches:
		if not match.playerA in players:
			players.append(match.playerA)
		if not match.playerB in players:
			players.append(match.playerB)
	return players

# -----------------------------------------------------------------

class CommunityBase:
	def __init__(self, tournamentList):
		self.players = list()
		for tournament in tournamentList:
			for currentPlayer in retrivePlayers(tournament.matches):
				if not currentPlayer in self.players:
					self.players.append(currentPlayer)

		self.base = dict()
		for winner in self.players:
			self.base[winner] = dict()
			for loser in self.players:
				self.base[winner][loser] = 0.

		for tournament in tournamentList:
			for match in tournament.matches:
				wins = match.calculateWins()
				self.base[match.playerA][match.playerB] += wins[0]
				self.base[match.playerB][match.playerA] += wins[1]
		pass

	def Get(self, winner, loser):
		return self.base[winner][loser]

	def CountWins(self, winner):
		wins = 0.
		for opponent in self.base[winner].keys():
			wins += self.base[winner][opponent]
		return wins

	def CountLinks(self, player):
		links = 0
		for opponent in self.players:
			if self.IsLinked(player, opponent):
				links += 1
		return links

	def IsLinked(self, player1, player2):
		return self.base[player1][player2] != 0 or self.base[player2][player1] != 0

# ----------------------------------------------------------------
if __name__ == "__main__":
	pass
	tournament1 = Tournament("tournament_results/2014-10-04_national.xml")
	#tournament2 = Tournament("tournament_logs/2014-07-05_msk_side_event.ant")

	#printTournament(tournament1, "!t1.txt")
	#printTournament(tournament2, "!t2.txt")
	pass
