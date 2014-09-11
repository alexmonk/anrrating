#-*- coding: utf-8 -*-
from tournament import Match

#-----------------------------------------

class PlayerPair:
	def __init__(self, player, opponent):
		self.player = player
		self.opponent = opponent
		self.wins = 0
		self.loses = 0

#-----------------------------------------

class Pairings:
	def __init__(self):
		self.players = dict()


	def addPlayer(self, player, opponent):
		if not player in self.players:
			self.players[player] = dict()
		if not opponent in self.players[player]:
			self.players[player][opponent] = PlayerPair(player, opponent)
		pass


	def addMatch(self, match):
		self.addPlayer(match.playerA, match.playerB)
		self.addPlayer(match.playerB, match.playerA)
		(winsA, winsB) = match.calculateWins()
		self.addPair(match.playerA, match.playerB, winsA, winsB)
		self.addPair(match.playerB, match.playerA, winsB, winsA)


	def addPair(self, player, opponent, wins, loses):
		self.players[player][opponent].wins += wins
		self.players[player][opponent].loses += loses
		pass


	def getTotalWins(self, player):
		wins = 0
		for opponent in self.players[player].keys():
			wins += self.players[player][opponent].wins
		return wins

	def getTotalGames(self, player):
		games = 0
		for opponent in self.players[player].keys():
			games += self.players[player][opponent].wins + self.players[player][opponent].loses
		return games

#-----------------------------------------
