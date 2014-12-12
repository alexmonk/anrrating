#-*- coding: utf-8 -*-
from power_level import PowerLevel
from tournament import retrivePlayers

#------------------------------------------------------------------

class P2PResult:
	def __init__(self):
		self.wins = 0.
		self.loses = 0.

	def update(self, wins, loses):
		self.wins += wins
		self.loses += loses

#------------------------------------------------------------------

class LeastSquaresRating:
	def __init__(self, matches):
		players = retrivePlayers(matches)
		self.results = dict()
		for playerA in players:
			self.results[playerA] = dict()
			for playerB in players:
				self.results[playerA][playerB] = P2PResult()

		for match in matches:
			playerA = match.playerA
			playerB = match.playerB
			(winA, winB) = match.calculateWins()
			self.results[playerA][playerB].update(winA, winB)
			self.results[playerB][playerA].update(winB, winA)

#------------------------------------------------------------------

	def calculatePowers(self, levels):
		powers = dict()
		for player in self.results.keys():
			powers[player] = PowerLevel(levels)


#------------------------------------------------------------------
