from Tkinter import *
from numpy import *

class Game:
	def __init__(self, N, M, numMines):
		self.N = N
		self.M = M
		self.numMines = min(numMines, N * M - 1)

		self.isMine = [False] * (N * M)

		# vector of directions
		self.directions = [-M - 1, -M, -M + 1, -1, 1, M - 1, M, M + 1]

		# number of adjacent bombs
		self.values = [0] * (N * M)
		
		# storing which tiles have been revealed to the player
		self.revealed = [False] * (N * M)
		
		# store the game state (0 - before start, 1 - running, 2 - ended)
		self.gameState = 0
		
		# store marked tiles: 0 - blank, 1 - flag, 2 - question mark
		self.flags = [0] * (N * M)

	def firstMove(self, tile):
		# generating mine locations
		permutation = [i for i in range(self.N * self.M)]
		permutation.pop(tile)
		self.mineLocations = random.permutation(permutation)[0 : self.numMines]
		for mine in self.mineLocations:
			self.isMine[mine] = True
		
		# calculating number of bombs adjecent to each tile
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

	def lost(self):
		self.gameState = 2
		for i in range(self.N * self.M):
			self.revealed[i] = True
			
	def flag(self, tile):
		# flag tile if it was not revealed already (if revealed, flag is always 0)
		if not self.revealed[tile]:
			self.flags[tile] = (self.flags[tile] + 1) % 3

	def reveal(self, startTile):
		# generate game grid on first move
		if not self.gameState:
			self.firstMove(startTile)
	
		# revealed a mine
		if startTile in self.mineLocations:
			self.revealed[startTile] = True
			self.lost()
			return [startTile]

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

		return changedTiles

class Minesweeper:
	def __init__(self, master):
		self.master = master

		# loading images
		self.tileImg = ["tile", "flag", "question"]
		for i in range(len(self.tileImg)):
			self.tileImg[i] = PhotoImage(file = "images/%s.gif" % self.tileImg[i])
		self.bombImg = PhotoImage(file = "images/bomb.gif")
		self.numberImg = []
		for i in range(9):
			self.numberImg.append(PhotoImage(file = "images/tile_%d.gif" % i))

		# generating a game for testing
		self.generate(15, 20, 50)

	# events that handle clicking on a tile
	def right_click(self, event):
		tile = int(event.widget.cget('text'))
		
		# only reveal a tile if it is not marked and not already revealed
		if not self.game.revealed[tile] and self.game.flags[tile] == 0:
			self.updateTiles(self.game.reveal(tile))
		
		# check if game ended and update all tiles
		if self.game.gameState == 2:
			self.updateTiles([i for i in range(self.game.N * self.game.M)])
			
	
	def left_click(self, event):
		tile = int(event.widget.cget('text'))
		self.game.flag(tile)
		self.updateTiles([tile])

	# find image that should be displayed on each tile
	def getImage(self, tile):
		if not self.game.revealed[tile]:
			return self.tileImg[self.game.flags[tile]]
		if self.game.isMine[tile]:
			return self.bombImg
		if self.game.values[tile] >= 0 and len(self.numberImg) > self.game.values[tile]:
			return self.numberImg[self.game.values[tile]]
		return self.numberImg[0]

	# update changed tiles
	def updateTiles(self, tiles):
		for tile in tiles:
			img = self.getImage(tile)
			self.mine_labels[tile].configure(image = img)
			self.mine_labels[tile].image = img

	def generate(self, N, M, num_mines):
		try:
			self.frame.destroy()
		except AttributeError:
			print("could not destroy current frame")

		self.game = Game(N, M, num_mines)

		self.frame = Frame(self.master)
		self.frame.pack()

		# creating labels
		self.mine_labels = []
		for i in range(N):
			for j in range(M):
				tile = j+i*M
				self.mine_labels.append(Label(self.frame, text = '%d' % tile,
					image = self.getImage(tile), borderwidth = 1, relief = "solid"))
				self.mine_labels[tile].grid(row = i, column = j)
				self.mine_labels[tile].bind('<1>', self.right_click)
				self.mine_labels[tile].bind('<2>', self.left_click)
				self.mine_labels[tile].bind('<3>', self.left_click)

def main():
	root = Tk()
	root.title("Minesweeper")
	minesweeper = Minesweeper(root)
	root.resizable(False, False)
	root.mainloop()

if __name__ == "__main__":
	main()
