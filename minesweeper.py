from Tkinter import *
from numpy import *

class Game:
	def __init__(self, N, M, numMines):
		self.N = N
		self.M = M
		self.numMines = numMines

		# generating mine locations
		self.isMine = [False] * (N * M)
		self.mineLocations = random.permutation(N * M)[0:numMines]
		for mine in self.mineLocations:
			self.isMine[mine] = True

		# vector of directions
		self.directions = [-M-1, -M, -M+1, -1, +1, M-1, M, M+1]

		# calculating number of bombs adjecent to each tile
		self.values = [0] * (N * M)
		for tile in range(N*M):
			if not self.isMine[tile]:
				for d in self.directions:
					if self.isValid(tile + d) and self.isAdjacent(tile, tile + d):
						if self.isMine[tile + d]:
							self.values[tile] += 1
		
		# storing which tiles have been revealed to the player
		self.revealed = [False] * (N * M)

	# check if two tiles are adjacent
	def isAdjacent(self, tile1, tile2):
		difRow = abs(tile1 // self.M - tile2 // self.M)
		difCol = abs(tile1 % self.M - tile2 % self.M)
		return difRow in range(2) and difCol in range(2)

	# check if tile is inside the grid
	def isValid(self, tile):
		return tile in range(self.N * self.M)

	def lost(self):
		print('lost')

	def reveal(self, startTile):
		# revealed a mine
		if startTile in self.mineLocations:
			self.revealed[tile] = True
			self.lost()
			return [startTile]

		queue = [startTile]
		changedTiles = []
		while len(queue):
			tile = queue.pop()
			if not self.revealed[tile]: 
				self.revealed[tile] = True
				changedTiles.append(tile)
				if not self.isMine[tile] and self.values[tile] == 0:
					for d in self.directions:
						if self.isValid(tile + d) and self.isAdjacent(tile, tile + d):
							queue.append(tile+d)

		return changedTiles

class Minesweeper:
	def __init__(self, master):
		self.master = master

		# loading images
		self.tile_img = PhotoImage(file = "images/tile.gif")
		self.bomb_img = PhotoImage(file = "images/bomb.gif")

		# generating a game for testing
		self.generate(15, 20, 50)

	# events that handle clicking on a tile
	def right_click(self, event):
		tile = int(event.widget.cget('text'))
		self.updateTiles(self.game.reveal(tile))
	
	def left_click(self, event):
		tile = int(event.widget.cget('text'))
		self.flags = (self.flags + 1) % 2

	# update changed tiles
	def updateTiles(tiles):
		pass

	def generate(self, N, M, num_mines):
		try:
			self.frame.destroy()
		except AttributeError:
			print("could not destroy current frame")

		self.game = Game(N, M, num_mines)
		# 0 - blank, 1 - flag, 2 - question mark
		self.flags = [0] * (N * M)

		self.frame = Frame(self.master)
		self.frame.pack()

		# creating labels
		self.mine_labels = []
		for i in range(N):
			for j in range(M):
				tile = j+i*M
				
				# choose image to put on tile
				img = self.tile_img
				if self.game.isMine[tile]:
					img = self.bomb_img

				self.mine_labels.append(Label(self.frame, text='%d' % tile, image=img, borderwidth=1))
				self.mine_labels[tile].grid(row=i, column=j)
				self.mine_labels[tile].bind('<1>', self.right_click)
				self.mine_labels[tile].bind('<3>', self.left_click)

def main():
	root = Tk()
	root.title("Minesweeper")
	minesweeper = Minesweeper(root)
	root.resizable(False, False)
	root.mainloop()

if __name__ == "__main__":
	main()
