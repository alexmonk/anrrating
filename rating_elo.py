#-*- coding: utf-8 -*-
import tournament
import math
from rating import PlayerRating
from pairings import Pairings

# -----------------------------------------------------------------

class EloRating:
	def __init__(self):
		self.players = dict()
		pass

	def updateByMatch(self, match, tournament):
		playerA = match.playerA
		playerB = match.playerB
		playerARating = self.getPlayerRating(playerA)
		playerBRating = self.getPlayerRating(playerB)

		(prestigeA, prestigeB) = match.calculatePrestige()
		changeCoefficient = 10 * match.getCountGames()

		newPlayerARating = self.calculateNewRating(playerARating, playerBRating, prestigeA/(prestigeA + prestigeB), changeCoefficient)
		newPlayerBRating = self.calculateNewRating(playerBRating, playerARating, prestigeB/(prestigeA + prestigeB), changeCoefficient)

		logA = self.toStringMatchResults(playerA, playerB, match.toStringPlayerAMatch(), newPlayerARating, newPlayerBRating)
		logB = self.toStringMatchResults(playerB, playerA, match.toStringPlayerBMatch(), newPlayerBRating, newPlayerARating)

		self.players[playerA].addMatch(tournament.name, tournament.date, playerB, newPlayerARating, logA)
		self.players[playerB].addMatch(tournament.name, tournament.date, playerA, newPlayerBRating, logB)
		pass


	def calculateNewRating(self, oldRating, opponentRating, score, changeCoefficient):
		ratingDifference = (opponentRating - oldRating)/400.
		scoreExpectation = 1./(1. + pow(10., ratingDifference))
		return oldRating + changeCoefficient * (score - scoreExpectation)


	def toStringMatchResults(self, playerA, playerB, matchDescription, newRatingA, newRatingB):
		ratingA = self.getPlayerRating(playerA)
		dA = newRatingA - ratingA
		ratingB = self.getPlayerRating(playerB)
		dB = newRatingB - ratingB
		return "(%.2f %+.3f) %s (%.2f %+.3f)" %(ratingA, dA, matchDescription, ratingB, dB)


	def getPlayerRating(self, player):
		if not player in self.players:
			self.players[player] = PlayerRating(player, "(ratingA +/- deltaA) nameA (corpA/runnerA) - (runnerB/corpB) nameB (ratingB +/- deltaB)", 1000)
		return self.players[player].getLastRating()


	def saveHistory(self, dirPath):
		for player in self.players.keys():
			self.players[player].saveHistory(dirPath + "/" + player + ".txt")
		pass

	def saveRatings(self, filePath, pairings):
		sortedPlayers = sorted(self.players.keys(), key=lambda x: self.players[x].getLastRating() * -1)
		text = ""
		for i in range(0, len(sortedPlayers)):
			player = sortedPlayers[i]
			text += str(i+1) + "\t" + player
			text += "\t%.2f" % self.players[player].getLastRating()
			text += "\t%i"%pairings.getTotalWins(player) + "/%i\n"%pairings.getTotalGames(player)
		file = open(filePath, 'w', encoding='utf8')
		file.write(text)
		file.close()

# -----------------------------------------------------------------
