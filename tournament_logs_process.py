#-*- coding: utf-8 -*-
import xmltodict
import dicttoxml
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

def createSwissMatchFromMatchDict(matchDict, gamesList):
	if matchDict["IsBYE"] == "true":
		return

	gameDict = dict()
	gameDict["player1"] = matchDict["Player1Alias"]
	gameDict["player2"] = matchDict["Player2Alias"]

	game1 = Game(matchDict["Player1Score1"], matchDict["Player2Score1"])
	game2 = Game(matchDict["Player1Score2"], matchDict["Player2Score2"])

	if matchDict["IsSecondGameNotStarted"] == "false" and game1.isZeroPoints() and game2.isZeroPoints():
		return
	if matchDict["IsSecondGameNotStarted"] == "true":
		gamesCount = 1
		if not game1.isZeroPoints():
			(prestige1, prestige2) = game1.calculatePrestige()
		else:
			(prestige1, prestige2) = game2.calculatePrestige()
	else:
		gamesCount = 2
		(prestige1game1, prestige2game1) = game1.calculatePrestige()
		(prestige1game2, prestige2game2) = game2.calculatePrestige()
		(prestige1, prestige2) = (prestige1game1 + prestige1game2, prestige2game1 + prestige2game2)

	gameDict["gamesCount"] = gamesCount
	gameDict["prestige1"] = prestige1
	gameDict["prestige2"] = prestige2
	gamesList.append(gameDict)

def createMatchesFromRoundDict(roundDict, gamesList):
	for matchDict in roundDict["Games"]["Game"]:
		createSwissMatchFromMatchDict(matchDict, gamesList)

def createMatchesFromRoundsDict(sourceDict, gamesList):
	if sourceDict == None:
		return

	if not isinstance(sourceDict["Round"], list):
		return createMatchesFromRoundDict(sourceDict["Round"], gamesList)
	for round in sourceDict["Round"]:
		createMatchesFromRoundDict(round, gamesList)

# ----------------------------

def createPlayoffMatchFromMatchDict(matchDict, gamesList):
	gameDict = dict()
	gameDict["player1"] = matchDict["Player1Alias"]
	gameDict["player2"] = matchDict["Player2Alias"]

	game1 = Game(matchDict["Player1Score1"], matchDict["Player2Score1"])
	game2 = Game(matchDict["Player1Score2"], matchDict["Player2Score2"])

	gamesCount = 0
	(prestige1, prestige2) = (0, 0)

	if not game1.isZeroPoints():
		gamesCount += 1
		(temp1, temp2) = game1.calculatePrestige()
		(prestige1, prestige2) = (prestige1 + temp1, prestige2 + temp2)
	if not game2.isZeroPoints():
		gamesCount += 1
		(temp1, temp2) = game2.calculatePrestige()
		(prestige1, prestige2) = (prestige1 + temp1, prestige2 + temp2)

	if gamesCount == 0:
		return

	gameDict["gamesCount"] = gamesCount
	gameDict["prestige1"] = prestige1
	gameDict["prestige2"] = prestige2
	gamesList.append(gameDict)

def createMatchesFromPlayoffDict(sourceDict, gamesList):
	if sourceDict == None:
		return

	sourceDict.pop("StartRound", None)
	for matchDict in sourceDict.values():
		createPlayoffMatchFromMatchDict(matchDict, gamesList)

# ----------------------------

def processLog(sourceFile, destFile):
	destDict = dict()
	file = open(sourceFile, 'r', encoding='utf8')
	sourceDict  = xmltodict.parse(file.read())
	sourceDict = sourceDict["Tournament"]
	file.close()

	destDict["header"] = dict()
	destDict["header"]["date"] = sourceDict["Date"]

	games = list()
	createMatchesFromRoundsDict(sourceDict["Rounds"], games)
	if "Playoffs" in sourceDict:
		createMatchesFromPlayoffDict(sourceDict["Playoffs"], games)
	if "Playoffs16" in sourceDict:
		createMatchesFromPlayoffDict(sourceDict["Playoffs16"], games)
	if "Playoffs8" in sourceDict:
		createMatchesFromPlayoffDict(sourceDict["Playoffs8"], games)

	destDict["games"] = games

	xml = dicttoxml.dicttoxml(destDict, attr_type=False)
	file = open(destFile, 'w', encoding='utf8')
	file.write(xml.decode("utf-8"))
	file.close()

def processLogs(sourceDir, destDir):
	tournaments = []
	for fileName in os.listdir(sourceDir):
		if os.path.isfile(sourceDir + fileName) and not os.path.isfile(destDir + fileName):
			processLog(sourceDir + fileName, destDir + fileName)

# -----------------------------------------------------------------

if __name__ == "__main__":
	pass
	processLogs("tournament_logs/", "tournament_results/")
	pass
