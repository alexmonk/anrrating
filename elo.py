
class EloResult:
    WIN = 1
    DRAW = 2
    LOSE = 3

class EloRatingSystem:
	def __init__(self):
		self.playerGameHistory = {}
		self.ratingTable = {}
		self.playedGames = {}
		pass
	def _saveHistoryString(self, string, p1Id, p2Id):
		def putStringForId(id):
			if id in self.playerGameHistory:
				self.playerGameHistory[id].append(string)
			else:
				defaultString = "(ratingA +/- deltaA) nameA (corpA/runnerA) - (runnerB, corpB) nameB (ratingB +/- deltaB)"
				self.playerGameHistory[id] = [defaultString, string]
			pass
		putStringForId(p1Id)
		putStringForId(p2Id)
		

	def calculateGame(self, player1Id, p1CorpPoints, p2RunnerPoints, p1RunnerPoints, p2CorpPoints, player2Id):
		if player1Id in self.ratingTable:
			ratingA = self.ratingTable[player1Id]
			self.playedGames[player1Id] += 1
		else:
			ratingA = 1000
			self.playedGames[player1Id] = 1

		if player2Id in self.ratingTable:
			ratingB = self.ratingTable[player2Id]
			self.playedGames[player2Id] += 1
		else:
			ratingB = 1000
			self.playedGames[player2Id] = 1

		scoreA = 0.0
		scoreB = 0.0
		if p1CorpPoints > p2RunnerPoints:
			scoreA += 0.5
		elif p2RunnerPoints > p1CorpPoints:
			scoreB += 0.5
		elif p2RunnerPoints == p1CorpPoints:
			scoreA += 0.25
			scoreB += 0.25

		if p1RunnerPoints > p2CorpPoints:
			scoreA += 0.5
		elif p2CorpPoints > p1RunnerPoints:
			scoreB += 0.5
		elif p2CorpPoints == p1RunnerPoints:
			scoreA += 0.25
			scoreB += 0.25
		
		newRA = self._recalculateEvo(ratingA, ratingB, scoreA, 20)
		newRB = self._recalculateEvo(ratingB, ratingA, scoreB, 20)
		self.ratingTable[player1Id] = newRA
		self.ratingTable[player2Id] = newRB

		dA = newRA - ratingA
		dB = newRB - ratingB
		historyString = "(%.2f %+.3f) %s (%i/%i) - (%i/%i) %s (%.2f %+.3f)" %(ratingA, dA, player1Id, p1CorpPoints, p1RunnerPoints, p2RunnerPoints, p2CorpPoints, player2Id, ratingB, dB)
		self._saveHistoryString(historyString, player1Id, player2Id)
		# self.playedGames[player2Id]+=1
		pass


	def _recalculateEvo(self, playerRating, opponentRating, playerScore, k):
		eA = 1.0 / (1.0 + pow(10.0, (opponentRating-playerRating)/400))
		newRating = playerRating + k * (playerScore - eA)
		return newRating


	def historyStringDict(self):
		strings = {}
		for name in self.playerGameHistory.keys():
			string = "\n".join(self.playerGameHistory[name])
			strings[name] = string
		return strings

	def ratingTableList(self):
		sortedTable = sorted(self.ratingTable.keys(), key=lambda x: self.ratingTable[x] * -1)
		strings = []
		for name in sortedTable:
			strings.append(str(name.encode("utf-8")) + "\t%.2f" % self.ratingTable[name] + "\t%i" % self.playedGames[name])
		return strings