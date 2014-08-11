#-*- coding: utf-8 -*-
import xmltodict
import os
from datetime import datetime

from tournament import Tournament
from tournament import createPlayersList
from rating_elo import EloRating
from rating_least_squares import LeastSquaresRating

# -----------------------------------------------------------------

def checkTournamentDates(tournaments): 	#debug
	dateError = False
	for tournament1 in tournaments:
		for tournament2 in tournaments:
			if tournament1 != tournament2 and tournament1.date == tournament2.date:
				print("Same date - " + tournament1.filePath + " - " + tournament2.filePath)
				dateError = True
	return dateError


def executeRatingCalculate():
	tournaments = []
	directoryWithLogs = "tournament_logs/"
	for fileName in os.listdir(directoryWithLogs):
		if os.path.isfile(directoryWithLogs + fileName):
			tournaments.append(Tournament(directoryWithLogs + fileName))

	tournaments = sorted(tournaments, key=lambda tournament: tournament.date)

	if checkTournamentDates(tournaments):
		return

	#debug
	players = []
	def addPlayer(playerName):
		if not playerName in players:
			print("Added player " + playerName)
			players.append(playerName)
	#end debug

	print("Calculating elo ratings")
	elo = EloRating()
	for tournament in tournaments:
		tournamentName = tournament.filePath.replace(directoryWithLogs, "")
		print(tournamentName)
		for match in tournament.matches:
			elo.updateByMatch(match, tournamentName)
			addPlayer(match.playerA) #debug
			addPlayer(match.playerB) #debug

	print("Done")

	elo.saveHistory("playerHistory")
	elo.saveRatings("netrunner_elo_rating.csv")

	#leastSquares = LeastSquaresRating(matches)
	pass


if __name__ == "__main__":
    executeRatingCalculate()
