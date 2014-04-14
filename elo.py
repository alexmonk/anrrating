
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
	def _saveHistoryString(self, string, pId):
		def putStringForId(id):
			if id in self.playerGameHistory:
				self.playerGameHistory[id].append(string)
			else:
				defaultString = "(ratingA +/- deltaA) nameA (corpA/runnerA) - (runnerB/corpB) nameB (ratingB +/- deltaB)"
				self.playerGameHistory[id] = [defaultString, string]
			pass
		putStringForId(pId)
		# putStringForId(p2Id)
		

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
			scoreA += 1
			if p1CorpPoints > 6:
				scoreA += 1
		elif p2RunnerPoints > p1CorpPoints:
			scoreB += 1
			if p2RunnerPoints > 6:
			 	scoreB += 1
		elif p2RunnerPoints == p1CorpPoints:# or (p2RunnerPoints < 7 and p1CorpPoints < 7):
			scoreA += 1
			scoreB += 1

		if p1RunnerPoints > p2CorpPoints:
			scoreA += 1
			if p1RunnerPoints > 6:
				scoreA += 1
		elif p2CorpPoints > p1RunnerPoints:
			scoreB += 1
			if p2CorpPoints > 6:
			 	scoreB += 1
		elif p2CorpPoints == p1RunnerPoints:# or (p2CorpPoints < 7 and p1RunnerPoints < 7):
			scoreA += 1
			scoreB += 1

		D = (4.0 - scoreA - scoreB )/8
		scoreA = scoreA / 4.0 + D
		scoreB = scoreB / 4.0 + D
		# print "A: %.2f B: %.2f" % (scoreA, scoreB)
		# print "D = %.2f" % (D)

		relativeScoreA = scoreA / (scoreA + scoreB)
		relativeScoreB = 1 - relativeScoreA
		# print "rA: %.2f rB: %.2f" % (relativeScoreA, relativeScoreB)

		newRA = self._recalculateEvo(ratingA, ratingB, relativeScoreA, 20)
		newRB = self._recalculateEvo(ratingB, ratingA, relativeScoreB, 20)
		self.ratingTable[player1Id] = newRA
		self.ratingTable[player2Id] = newRB

		dA = newRA - ratingA
		dB = newRB - ratingB
		# historyStringA = "(%.2f %+.3f) %s (%i/%i = %.2f) - (%i/%i = %.2f) %s (%.2f %+.3f)" %(ratingA, dA, player1Id, p1CorpPoints, p1RunnerPoints, scoreA, p2RunnerPoints, p2CorpPoints, scoreB, player2Id, ratingB, dB)
		# historyStringB = "(%.2f %+.3f) %s (%i/%i = %.2f) - (%i/%i = %.2f) %s (%.2f %+.3f)" %(ratingB, dB, player2Id, p2CorpPoints, p2RunnerPoints, scoreB, p1RunnerPoints, p1CorpPoints, scoreA, player1Id, ratingA, dA)
		historyStringA = "(%.2f %+.3f) %s (%i/%i) - (%i/%i) %s (%.2f %+.3f)" %(ratingA, dA, player1Id, p1CorpPoints, p1RunnerPoints, p2RunnerPoints, p2CorpPoints, player2Id, ratingB, dB)
		historyStringB = "(%.2f %+.3f) %s (%i/%i) - (%i/%i) %s (%.2f %+.3f)" %(ratingB, dB, player2Id, p2CorpPoints, p2RunnerPoints, p1RunnerPoints, p1CorpPoints, player1Id, ratingA, dA)

		self._saveHistoryString(historyStringA, player1Id)
		self._saveHistoryString(historyStringB, player2Id)
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