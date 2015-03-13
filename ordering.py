#-*- coding: utf-8 -*-


#-------------------------------------------------------------

class Position:
	def __init__(self, pos, name):
		self.pathIndex = pos
		self.minPos = pos
		self.maxPos = pos
		self.name = name
		pass

class FinalOrdering:
	def __init__(self, distance, path, outFile):
		positions = list()
		for i in range(0, len(path)):
			current = path[i]
			position = Position(i, current)
			lowPos = -1
			for low in range(0, i):
				if distance.Get(current, path[low]) != 0 or distance.Get(path[low], current) != 0:
					lowPos = low
			highPos = len(path)
			for high in range(i+1, len(path)):
				if distance.Get(current, path[high]) != 0 or distance.Get(path[high], current) != 0:
					highPos = high
					break
			position.minPos = lowPos + 1
			position.maxPos = highPos - 1
			positions.append(position)
		pass

		indexChanges = [i for i in range(0, len(path))]
		index = 0
		set = self.GetIndexSet(0, positions)
		for i in range(1, len(path)):
			newSet = self.GetIndexSet(i, positions)
			if newSet != set:
				index += 1
			set = newSet
			indexChanges[i] = index
		pass

		trimedPositions = list()
		for position in positions:
			position.minPos = indexChanges[position.minPos]
			position.maxPos = indexChanges[position.maxPos]
			trimedPositions.append(position)
		self.DumpResults(trimedPositions, path, outFile)


	def DumpResults(self, positions, players, outFile):
		positions = sorted(positions, key=lambda x: (x.minPos, x.maxPos))
		text = ""
		for i in range(0, len(positions)):
			player = players[i]
			if positions[i].minPos == positions[i].maxPos:
				text += str(positions[i].minPos+1)
			else:
				text += str(positions[i].minPos+1) + "-" + str(positions[i].maxPos+1)
			text += "," + players[i] + "\n"
		file = open(outFile, 'w', encoding='utf8')
		file.write(text)
		file.close()
		pass

	def GetIndexSet(self, index, positions):
		result = list()
		for position in positions:
			if position.minPos <= index <= position.maxPos:
				result.append(position.name)
		return sorted(result)

#-------------------------------------------------------------

class Ordering:
	def __init__(self, distance, outFile):
		self.distance = distance
		self.minPaths = list()
		result = self.Process()
		FinalOrdering(distance, result, outFile)


	def FindAlreadyCalculatedMinPath(self, set):
		if len(set) <= 1:
			return set
		sortedSet = sorted(set)
		for path in self.minPaths:
			if sortedSet == sorted(path):
				return path
		return None

	def AddAlreadyCalculatedMinPath(self, path):
		if len(path) >= 2:
			self.minPaths.append(path)


	def Process(self):
		return self.GetMinPath(self.distance.nodes)


	def GetMinPath(self, set):
		result = self.FindAlreadyCalculatedMinPath(set)
		if result != None:
			return result

		result = list()
		for node in set:
			result = self.AddNode(node, result)
		return result


	def CalculateLengthBetween(self, highNodes, lowNodes):
		length = 0.
		for high in highNodes:
			for low in lowNodes:
				length += self.distance.Get(high, low)
		return length


	def GetDefaultSubPaths(self, node, path):
		minLength = None
		high = None
		low = None
		for i in range(0, len(path)+1):
			currentLength = 0.
			currentLength += self.CalculateLengthBetween(path[0:i], [node])
			currentLength += self.CalculateLengthBetween([node], path[i:])
			if minLength == None or minLength >= currentLength:
				minLength = currentLength
				high = path[0:i]
				low = path[i:]
		return (high, low)


	def GetProblemNodes(self, node, subPaths):
		highProblems = list()
		lowProblems = list()
		for high in subPaths[0]:
			if self.distance.Get(high, node) > self.distance.Get(node, high):
				highProblems.append(high)
		for low in subPaths[1]:
			if self.distance.Get(node, low) > self.distance.Get(low, node):
				lowProblems.append(low)
		return (highProblems, lowProblems)


	def GetNewHighStep(self, node, path, problems):
		changeNode = None
		step = 1.
		for problem in problems:
			i = path.index(problem)
			middle = path[(i+1):]
			middleDifference = self.CalculateLengthBetween(middle, [problem]) - self.CalculateLengthBetween([problem], middle)
			nodeDifference = self.distance.Get(problem, node) - self.distance.Get(node, problem)
			currentStep = float(middleDifference)/float(nodeDifference)
			if currentStep < step:
				step = currentStep
				changeNode = problem
		return (step, changeNode)

	def GetNewLowStep(self, node, path, problems):
		changeNode = None
		step = 1.
		for problem in problems:
			i = path.index(problem)
			middle = path[0:i]
			middleDifference = self.CalculateLengthBetween([problem], middle) - self.CalculateLengthBetween(middle, [problem])
			nodeDifference = self.distance.Get(node, problem) - self.distance.Get(problem, node)
			currentStep = float(middleDifference)/float(nodeDifference)
			if currentStep < step:
				step = currentStep
				changeNode = problem
		return (step, changeNode)


	def AddNode(self, node, path):
		subPaths = self.GetDefaultSubPaths(node, path)
		problems = self.GetProblemNodes(node, subPaths)
		step = 0.
		while step < 1. and (len(problems[0]) != 0 or len(problems[1]) != 0):
			highStep = self.GetNewHighStep(node, subPaths[0], problems[0])
			lowStep = self.GetNewLowStep(node, subPaths[1], problems[1])
			if highStep[0] < step or lowStep[0] < step:
				#raise Exception("Step error")
				pass
			if highStep[0] >= 1. and lowStep[0] >= 1.:
				break

			if highStep[0] < lowStep[0]:
				subPaths[0].remove(highStep[1])
				subPaths[1].append(highStep[1])
				step = highStep[0]
			else:
				subPaths[0].append(lowStep[1])
				subPaths[1].remove(lowStep[1])
				step = lowStep[0]

			problems = self.GetProblemNodes(node, subPaths)
			subPaths = (self.GetMinPath(subPaths[0]), self.GetMinPath(subPaths[1]))
		result = subPaths[0] + [node] + subPaths[1]
		self.AddAlreadyCalculatedMinPath(result)
		return result

#-------------------------------------------------------------
