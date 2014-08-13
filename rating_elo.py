#-*- coding: utf-8 -*-
import tournament
import math

# -----------------------------------------------------------------

class EloPlayerRating:
	def __init__(self):
		self.rating = 1000
		self.history = []
		self.history.append(["", "(ratingA +/- deltaA) nameA (corpA/runnerA) - (runnerB/corpB) nameB (ratingB +/- deltaB)"])
		self.playedGames = 0

	def updateRating(self, newRating, tournamentName, logText):
		self.rating = newRating
		if self.history[len(self.history) - 1][0] != tournamentName:
			self.history.append([tournamentName])
		self.history[len(self.history) - 1].append(str(logText))
		self.playedGames += 1

# -----------------------------------------------------------------

class EloRating:
	def __init__(self):
		self.players = dict()
		pass


	def updateByMatch(self, match, tournamentName):
		playerA = match.playerA
		playerB = match.playerB
		playerARating = self.getPlayerRating(playerA)
		playerBRating = self.getPlayerRating(playerB)

		(prestigeA, prestigeB) = match.calculatePrestige()
		changeCoefficient = 10 * match.getCountGames()

		newPlayerARating = self.calculateNewRating(playerARating, playerBRating, prestigeA/(prestigeA + prestigeB), changeCoefficient)
		newPlayerBRating = self.calculateNewRating(playerBRating, playerARating, prestigeB/(prestigeA + prestigeB), changeCoefficient)

		pointsA = match.toStringPlayerAPoints()
		pointsB = match.toStringPlayerBPoints()

		logA = self.toStringMatchResults(playerA, playerB, pointsA, pointsB, newPlayerARating, newPlayerBRating)
		logB = self.toStringMatchResults(playerB, playerA, pointsB, pointsA, newPlayerBRating, newPlayerARating)

		self.players[playerA].updateRating(newPlayerARating, tournamentName, logA)
		self.players[playerB].updateRating(newPlayerBRating, tournamentName, logB)
		pass


	def calculateNewRating(self, oldRating, opponentRating, score, changeCoefficient):
		ratingDifference = (opponentRating - oldRating)/400.
		scoreExpectation = 1./(1. + pow(10., ratingDifference))
		return oldRating + changeCoefficient * (score - scoreExpectation)


	def toStringMatchResults(self, playerA, playerB, pointsA, pointsB, newRatingA, newRatingB):
		ratingA = self.getPlayerRating(playerA)
		dA = newRatingA - ratingA
		ratingB = self.getPlayerRating(playerB)
		dB = newRatingB - ratingB
		return "(%.2f %+.3f) %s %s - %s %s (%.2f %+.3f)" %(ratingA, dA, playerA, pointsA, pointsB, playerB, ratingB, dB)


	def getPlayerRating(self, player):
		if not player in self.players:
			self.players[player] = EloPlayerRating()
		return self.players[player].rating


	def saveHistory(self, dirPath):
		for player in self.players.keys():
			historyStr = ""
			tournaments = self.players[player].history
			for tournament in tournaments:
				if len(tournament) > 1:
					for log in tournament:
						historyStr += "\n" + log
			filePath = dirPath + "/" + player + ".txt"
			file = open(filePath, 'w', encoding='utf8')
			file.write(historyStr)
			file.close()

	def saveRatings(self, filePath):
		sortedPlayers = sorted(self.players.keys(), key=lambda x: self.players[x].rating * -1)
		text = ""
		for player in sortedPlayers:
			#tableStr.append(str(player.encode("utf-8")) + "\t%.2f" % self.players[player].rating + "\t%i" % self.players[player].playedGames)
			text += player + "\t%.2f" % self.players[player].rating + "\t%i\n" % self.players[player].playedGames
		#file = open(filePath, 'w')
		file = open(filePath, 'w', encoding='utf8')
		file.write(text)
		file.close()

# -----------------------------------------------------------------
