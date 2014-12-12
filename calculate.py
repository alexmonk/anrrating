#-*- coding: utf-8 -*-
import xmltodict
import os
from datetime import datetime

from tournament import Tournament
from tournament import retrivePlayers
from tournament_logs_process import processLogs
from pairings import Pairings
from rating_elo import EloRating
from rating_least_squares import LeastSquaresRating

# -----------------------------------------------------------------

def checkTournamentDates(tournaments):
	dateError = False
	for tournament1 in tournaments:
		for tournament2 in tournaments:
			if tournament1 != tournament2 and tournament1.date == tournament2.date:
				print("Same date - " + tournament1.filePath + " - " + tournament2.filePath)
				dateError = True
	return dateError

# -----------------------------------------------------------------

def executeRatingCalculate():
	processLogs("tournament_logs/", "tournament_results/")

	tournaments = []
	players = []
	directoryWithLogs = "tournament_results/"
	for fileName in os.listdir(directoryWithLogs):
		if os.path.isfile(directoryWithLogs + fileName):
			currentTournament = Tournament(directoryWithLogs + fileName)
			tournaments.append(currentTournament)
			currentPlayers = retrivePlayers(currentTournament.matches)
			for player in currentPlayers:
				if not player in players:
					print(player)
					players.append(player)

	tournaments = sorted(tournaments, key=lambda tournament: tournament.date)

	if checkTournamentDates(tournaments):
		return

	print("Calculating elo ratings")
	elo = EloRating()
	pairings = Pairings()
	for tournament in tournaments:
		for match in tournament.matches:
			pairings.addMatch(match)
			elo.updateByMatch(match, tournament)

	print("Done")

	if not os.path.exists("playerHistory"):
		os.makedirs("playerHistory")
	elo.saveHistory("playerHistory")
	elo.saveRatings("netrunner_elo_rating.csv", pairings)

	#leastSquares = LeastSquaresRating(matches)
	pass


if __name__ == "__main__":
    executeRatingCalculate()
