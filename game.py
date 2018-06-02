from numpy import *

class Game:
	def __init__(self, N, M, numMines):
		self.N = N
		self.M = M
		self.numMines = min(numMines, N * M - 1)

		self.isMine = [False] * (N * M)

		# vector of directions
		self.directions = [-M - 1, -M, -M + 1, -1, 1, M - 1, M, M + 1]
		# getting unique values
		self.directions = list(set(self.directions))

		# number of adjacent mines
		self.values = [0] * (N * M)
		
		# storing which tiles have been revealed to the player
		self.revealed = [False] * (N * M)
		
		# store the game state (0 - before start, 1 - running, 2 - ended)
		self.gameState = 0
		self.won = False
		
		# store marked tiles: 0 - blank, 1 - flag, 2 - question mark
		self.flags = [0] * (N * M)
		self.numFlags = 0

	def firstMove(self, tile):
		# generating mine locations
		permutation = [i for i in range(self.N * self.M)]
		permutation.pop(tile)
		self.mineLocations = random.permutation(permutation)[0 : self.numMines]
		for mine in self.mineLocations:
			self.isMine[mine] = True
		
		# calculating number of mines adjecent to each tile
		for tile in range(self.N * self.M):
			if not self.isMine[tile]:
				for d in self.directions:
					if self.isAdjacent(tile, tile + d):
						if self.isMine[tile + d]:
							self.values[tile] += 1
		
		# game started
		self.gameState = 1

	# check if two tiles are adjacent and valid
	def isAdjacent(self, tile1, tile2):
		difRow = abs(tile1 // self.M - tile2 // self.M)
		difCol = abs(tile1 % self.M - tile2 % self.M)
		isValid = self.isValid(tile1) and self.isValid(tile2)
		return difRow in range(2) and difCol in range(2) and isValid

	# check if tile is inside the grid
	def isValid(self, tile):
		return tile in range(self.N * self.M)
		
	def flag(self, tile):
		# flag tile if it was not revealed already (if revealed, flag is always 0)
		if not self.revealed[tile]:
			if self.flags[tile] == 1:
				self.numFlags -= 1
			self.flags[tile] = (self.flags[tile] + 1) % 3
			if self.flags[tile] == 1:
				self.numFlags += 1
	
	def ended(self, won, tile):
		self.gameState = 2
		self.won = won

		for i in range(self.N * self.M):
			self.revealed[i] = True

			# setting wrong flags to 3
			if self.flags[i] == 1 and not self.isMine[i]:
				self.flags[i] = 3

		if won:
			#setting flags on unflagged mines
			for mine in self.mineLocations:
				self.flags[mine] = 1
		else:
			# setting clicked bomb flag to 4
			self.flags[tile] = 4
	
	def hasEnded(self):
		# check if a mine was revealed
		for mine in self.mineLocations:
			if self.revealed[mine]:
				self.ended(False, mine)
				return True

		# check if any non-mine tile was not revealed
		for tile in range(self.N * self.M):
			if not self.revealed[tile] and not self.isMine[tile]:
				return False
		
		# if all non-mine tiles were revealed, game ended
		self.ended(True, 0)
		return True

	def reveal(self, startTile):
		# generate game grid on first move
		if not self.gameState:
			self.firstMove(startTile)
	
		queue = [startTile]
		changedTiles = []
		while len(queue):
			tile = queue.pop()
			if not self.revealed[tile]: 
				self.revealed[tile] = True
				self.flags[tile] = 0
				changedTiles.append(tile)
				# only reveal adjacent cells if the current cell is not a number or mine
				if not self.isMine[tile] and self.values[tile] == 0:
					for d in self.directions:
						# only reveal tile if it is not flagged
						if self.isAdjacent(tile, tile + d) and self.flags[tile + d] == 0:
							queue.append(tile+d)
		if self.hasEnded():
			return [i for i in range(self.N * self.M)]	
		else:
			return changedTiles
