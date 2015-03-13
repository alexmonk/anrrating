#-*- coding: utf-8 -*-

import math

#-----------------------------------------

class GamesDistance:
	def __init__(self, base):
		self.nodes = base.players
		self.base = base

	def Get(self, high, low):
		return self.base.Get(low, high)

#-----------------------------------------

class LeastSquares:
	def __init__(self, base):
		self.nodes = base.players
		self.base = base

	def Get(self, high, low):
		highValue = self.base.Get(high, low)
		lowValue = self.base.Get(low, high)
		if highValue > lowValue:
			return 0.
		else:
			dif = highValue - lowValue
			dif = float(dif)/2.
			return dif*dif

#-----------------------------------------

class MaximumLikehood:
	def __init__(self, base):
		self.nodes = base.players
		self.base = base

	def Get(self, high, low):
		highValue = self.base.Get(high, low)
		lowValue = self.base.Get(low, high)
		total = highValue + lowValue
		if total == 0:
			return 0

		if highValue > lowValue:
			prob = highValue/total
			highProb = 0.
			lowProb = 0.
			if highValue > 0:
				highProb = -highValue*math.log2(prob)
			if lowValue > 0:
				lowProb = -lowValue*math.log2(1.-prob)
			return highProb + lowProb
		else:
			return total*math.log2(2)

#-----------------------------------------

class Linkage:
	def __init__(self, base):
		self.nodes = sorted(base.players, key=lambda x: base.CountLinks(x)*-1)
		self.base = base
		self.results = list()

		self.BronKerbosch(list(), self.nodes, list())
		return

#----------------

	def AddResult(self, set):
		set = sorted(set)
		if len(self.results) == 0:
			self.results.append(set)
			return
		if len(self.results[0]) > len(set):
			return
		if len(self.results[0]) < len(set):
			self.results.clear()
		if not set in self.results:
			self.results.append(set)

	def GetNeigbours(self, node, set):
		results = list()
		for it in set:
			if self.base.IsLinked(node, it):
				results.append(it)
		return results

	def BronKerbosch(self, set, possibleSet, notSet):
		if len(possibleSet) == 0 and len(notSet) == 0:
			self.AddResult(set)
			return
		for possible in possibleSet:
			self.BronKerbosch(list(set) + [possible], self.GetNeigbours(possible, possibleSet), self.GetNeigbours(possible, notSet))
			possibleSet.remove(possible)
			notSet.append(possible)
			pass

#----------------
