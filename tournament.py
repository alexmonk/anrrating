#-*- coding: utf-8 -*-
import xmltodict
import os
import collections
from datetime import datetime

# ----------------------------

class Game:
	def __init__(self, playerAPoints, playerBPoints):
		self.playerAPoints = int(playerAPoints)
		self.playerBPoints = int(playerBPoints)
		if self.playerAPoints >= 7 and self.playerBPoints >= 7:
			raise RuntimeError("In a game both players have more than 6 points")

	def calculatePrestige(self):
		if self.playerAPoints >= 7:
			return (2, 0)

		if self.playerBPoints >= 7:
			return (0, 2)

		if self.playerAPoints == self.playerBPoints:
			return (1, 1)

		if self.playerAPoints > self.playerBPoints:
			return (1, 0)
		else:
			return (0, 1)

		pass

	def calculateWins(self):
		(prestigeA, prestigeB) = self.calculatePrestige()
		if prestigeA > prestigeB:
			return (1., 0.)
		if prestigeA < prestigeB:
			return (0., 1.)
		return (0.5, 0.5)

	def isZeroPoints(self):
		return self.playerAPoints == 0 and self.playerBPoints == 0

# ----------------------------

class Match:
	def __init__(self, playerA, playerB):
		self.playerA = playerA
		self.playerB = playerB
		self.games = []

	def addGame(self, game):
		self.games.append(game)


	def calculatePrestige(self):
		(prestigeA, prestigeB) = (0, 0)
		for game in self.games:
			(curPrestigeA, curPrestigeB) = game.calculatePrestige()
			(prestigeA, prestigeB) = (prestigeA + curPrestigeA, prestigeB + curPrestigeB)
		return (prestigeA, prestigeB)


	def calculateWins(self):
		(winsA, winsB) = (0, 0)
		for game in self.games:
			(curWinsA, curWinsB) = game.calculateWins()
			(winsA, winsB) = (winsA + curWinsA, winsB + curWinsB)
		return (winsA, winsB)


	def toStringPlayerAPoints(self):
		pointsString = ""
		for game in self.games:
			if pointsString != "":
				pointsString += "/" + str(game.playerAPoints)
			else:
				pointsString += str(game.playerAPoints)
		return "(" + pointsString + ")"


	def toStringPlayerBPoints(self):
		pointsString = ""
		for game in self.games:
			if pointsString != "":
				pointsString += "/" + str(game.playerBPoints)
			else:
				pointsString += str(game.playerBPoints)
		return "(" + pointsString + ")"

	def toStringPlayerAMatch(self):
		return self.playerA + " " + self.toStringPlayerAPoints() + " - " + self.toStringPlayerBPoints() + " " + self.playerB

	def toStringPlayerBMatch(self):
		return self.playerB + " " + self.toStringPlayerBPoints() + " - " + self.toStringPlayerAPoints() + " " + self.playerA

	def getCountGames(self):
		return len(self.games)

# ----------------------------

def createSwissMatchFromMatchDict(matchDict):
	if matchDict["IsBYE"] == "true":
		return None

	match = Match(matchDict["Player1Alias"], matchDict["Player2Alias"])

	game1 = Game(matchDict["Player1Score1"], matchDict["Player2Score1"])
	game2 = Game(matchDict["Player1Score2"], matchDict["Player2Score2"])
	if matchDict["IsSecondGameNotStarted"] == "false" and game1.isZeroPoints() and game2.isZeroPoints():
		return None
	if matchDict["IsSecondGameNotStarted"] == "true":
		if not game1.isZeroPoints():
			match.addGame(game1)
		else:
			match.addGame(game2)
	else:
		match.addGame(game1)
		match.addGame(game2)
	return match


def createPlayoffMatchFromMatchDict(matchDict):
	match = Match(matchDict["Player1Alias"], matchDict["Player2Alias"])

	def addPlayoffGame(pointsA, pointsB):
		if int(pointsA) != 0 or int(pointsB) != 0:
			match.addGame(Game(pointsA, pointsB))

	game1 = Game(matchDict["Player1Score1"], matchDict["Player2Score1"])
	if not game1.isZeroPoints():
		match.addGame(game1)
	game2 = Game(matchDict["Player1Score2"], matchDict["Player2Score2"])
	if not game2.isZeroPoints():
		match.addGame(game2)
	if match.getCountGames() == 0:
		return None
	return match

# ----------------------------

def createMatchesFromRoundDict(roundDict):
	matches = []
	for matchDict in roundDict["Games"]["Game"]:
		match = createSwissMatchFromMatchDict(matchDict)
		if match != None:
			matches.append(match)
	return matches

# ----------------------------

def createMatchesFromRoundsDict(roundsDict):
	if roundsDict == None:
		return []
	matches = []

	if not isinstance(roundsDict["Round"], list):
		return createMatchesFromRoundDict(roundsDict["Round"])
	for round in roundsDict["Round"]:
		matches += createMatchesFromRoundDict(round)
	return matches

# ----------------------------

def createMatchesFromPlayoffDict(playoffDict):
	if playoffDict == None:
		return []
	matches = []
	playoffDict.pop("StartRound", None)
	for matchDict in playoffDict.values():
		match = createPlayoffMatchFromMatchDict(matchDict)
		if match != None:
			matches.append(match)
	return matches

# ----------------------------

class Tournament:
	def __init__(self, filePath):
		self.name = filePath
		file = open(filePath, 'r', encoding='utf8')
		tournamentDict  = xmltodict.parse(file.read())
		tournamentDict = tournamentDict["Tournament"]
		file.close()

		print("Parsing " + filePath)

		self.date = datetime.strptime(tournamentDict["Date"][:13], '%Y-%m-%dT%H')  #2014-02-24T00:00:00+04:00
		print(self.date)
		self.matches = createMatchesFromRoundsDict(tournamentDict["Rounds"])
		if "Playoffs" in tournamentDict:
			self.matches += createMatchesFromPlayoffDict(tournamentDict["Playoffs"])
		if "Playoffs16" in tournamentDict:
			self.matches += createMatchesFromPlayoffDict(tournamentDict["Playoffs16"])
		if "Playoffs8" in tournamentDict:
			self.matches += createMatchesFromPlayoffDict(tournamentDict["Playoffs8"])

		print("Done")

# ----------------------------

def createPlayersList(matches):
	players = []
	for match in matches:
		if not match.playerA in players:
			players.append(match.playerA)
		if not match.playerB in players:
			players.append(match.playerB)
	return players

# -----------------------------------------------------------------
# -----------------------------------------------------------------

def printTournament(tournament, filePath):
	file = open(filePath, "w", encoding="utf8")
	for match in tournament.matches:
		logText = match.playerA + " " + match.toStringPlayerAPoints() + " " + match.toStringPlayerBPoints() + " " + match.playerB + "\r\n"
		file.write(logText)
	file.close()


if __name__ == "__main__":
	pass
	#tournament1 = Tournament("tournament_logs/2014-07-05_msk_regional.ant")
	#tournament2 = Tournament("tournament_logs/2014-07-05_msk_side_event.ant")

	#printTournament(tournament1, "!t1.txt")
	#printTournament(tournament2, "!t2.txt")
	pass
