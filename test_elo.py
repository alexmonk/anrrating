from elo import EloRatingSystem

eloRatingSystem = EloRatingSystem()
eloRatingSystem.calculateGame("4:0", 10, 0, 10, 0, "0:4")
eloRatingSystem.calculateGame("3:1", 10, 0, 3, 3, "1:3")
eloRatingSystem.calculateGame("2:2", 10, 0, 0, 10, "2:2")
eloRatingSystem.calculateGame("3:0", 10, 0, 5, 0, "0:3")
eloRatingSystem.calculateGame("2:1", 10, 0, 0, 4, "0:3")
history = eloRatingSystem.historyStringDict()
for player in history.keys():
	historyString = history[player]
	if historyString != "(ratingA +/- deltaA) nameA (corpA/runnerA) - (runnerB, corpB) nameB (ratingB +/- deltaB)\r\n":
		print historyString