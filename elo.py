class EloRatingObject:
	def __init__(self):
		self.commonRating = 1000
		self.runnerRating = 1000
		self.corpRating = 1000


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

	# def _

	def _getRatingTupleForIds(self, player1Id, player2Id):
		if player1Id in self.ratingTable:
			ratingAObject = self.ratingTable[player1Id]
			self.playedGames[player1Id] += 1
		else:
			ratingAObject = EloRatingObject()
			self.playedGames[player1Id] = 1

		if player2Id in self.ratingTable:
			ratingBObject = self.ratingTable[player2Id]
			self.playedGames[player2Id] += 1
		else:
			ratingBObject = EloRatingObject()
			self.playedGames[player2Id] = 1
		return (ratingAObject, ratingBObject)

	def calculateGame(self, player1Id, p1CorpPoints, p2RunnerPoints, p1RunnerPoints, p2CorpPoints, player2Id):
		ratingTuple = self._getRatingTupleForIds(player1Id, player2Id)
		ratingAObject = ratingTuple[0]
		ratingBObject = ratingTuple[1]
		runScoreA = 0.0
		corpScoreA = 0.0

		runScoreB = 0.0
		corpScoreB = 0.0

		ratingA = ratingAObject.commonRating
		ratingB = ratingBObject.commonRating

		if p1CorpPoints > p2RunnerPoints: 
			corpScoreA += 1
			if p1CorpPoints > 6:
				corpScoreA += 1
		elif p2RunnerPoints > p1CorpPoints:
			runScoreB += 1
			if p2RunnerPoints > 6:
			 	runScoreB += 1
		elif p2RunnerPoints == p1CorpPoints:
			corpScoreA += 1
			runScoreB += 1

		if p1RunnerPoints > p2CorpPoints:
			runScoreA += 1
			if p1RunnerPoints > 6:
				runScoreA += 1
		elif p2CorpPoints > p1RunnerPoints:
			corpScoreB += 1
			if p2CorpPoints > 6:
			 	corpScoreB += 1
		elif p2CorpPoints == p1RunnerPoints:
			runScoreA += 1
			corpScoreB += 1

		scoreA = runScoreA + corpScoreA
		scoreB = runScoreB + corpScoreB

		D = (4.0 - scoreA - scoreB )/8
		scoreA = scoreA / 4.0 + D
		scoreB = scoreB / 4.0 + D

		relativeScoreA = scoreA / (scoreA + scoreB)
		relativeScoreB = 1 - relativeScoreA

		relativeRunScoreA = runScoreA / (runScoreA + corpScoreB)
		# print "rA: %.2f rB: %.2f" % (relativeScoreA, relativeScoreB)

		ratingAObject.commonRating = self._recalculateEvo(ratingA, ratingB, relativeScoreA, 20)
		ratingBObject.commonRating = self._recalculateEvo(ratingB, ratingA, relativeScoreB, 20)
		self.ratingTable[player1Id] = ratingAObject
		self.ratingTable[player2Id] = ratingBObject

		dA = ratingAObject.commonRating - ratingA
		dB = ratingBObject.commonRating - ratingB
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
		sortedTable = sorted(self.ratingTable.keys(), key=lambda x: self.ratingTable[x].commonRating * -1)
		strings = []
		for name in sortedTable:
			strings.append(str(name.encode("utf-8")) + "\t%.2f" % self.ratingTable[name].commonRating + "\t%i" % self.playedGames[name])
		return strings