from Tkinter import *
from game import *
import threading, time

class Minesweeper:
	def __init__(self, master):
		self.master = master

		# loading images
		self.tileImg = ["tile", "flag", "question", "flag_wrong", "bomb_clicked"]
		for i in range(len(self.tileImg)):
			self.tileImg[i] = PhotoImage(file = "images/%s.gif" % self.tileImg[i])
		self.bombImg = PhotoImage(file = "images/bomb.gif")
		self.numberImg = []
		for i in range(9):
			self.numberImg.append(PhotoImage(file = "images/tile_%d.gif" % i))

		# text to show on ui
		self.minesMessage = 'Remaining Mines: %d'
		self.endMessage = ['You Lost!', 'You Won!']
		
		# default game size
		self.generate(10, 10, 10)

	# events that handle clicking on a tile
	def right_click(self, event):
		tile = int(event.widget.cget('text'))
		
		# only reveal a tile if it is not marked and not already revealed
		if not self.game.revealed[tile] and self.game.flags[tile] == 0:
			self.updateTiles(self.game.reveal(tile))
		
	def left_click(self, event):
		tile = int(event.widget.cget('text'))
		self.game.flag(tile)
		self.updateTiles([tile])

	# find image that should be displayed on each tile
	def getImage(self, tile):
		# if tile was not revealed, use the tile flag
		# also, special cases for flags (wrong flag and clicked bomb)
		if not self.game.revealed[tile] or self.game.flags[tile] > 2:
			return self.tileImg[self.game.flags[tile]]
		else:
			# if bomb was flagged, keep the flag
			if self.game.isMine[tile]:
				if self.game.flags[tile] == 1:
					return self.tileImg[self.game.flags[tile]]
				else:
					return self.bombImg
			return self.numberImg[self.game.values[tile]]

	# update changed tiles
	def updateTiles(self, tiles):
		for tile in tiles:
			img = self.getImage(tile)
			self.mineLabels[tile].configure(image = img)
			self.mineLabels[tile].image = img

		# change number of remaining mines
		remainingMines = self.game.numMines - self.game.numFlags
		# if game ended, change the message
		if self.game.gameState == 2:
			newText = self.endMessage[int(self.game.won)]
		else:
			newText = self.minesMessage % remainingMines
		self.minesLabel.configure(text = newText)
		self.minesLabel.text = newText
		
	def generate(self, N, M, numMines):
		# clear frames so a new game can be created
		try:
			self.gameFrame.destroy()
			self.infoFrame.destroy()
			self.popup.destroy()
		except AttributeError:
			print("could not destroy current frames")

		self.game = Game(N, M, numMines)
		
		# frame that holds the game
		self.gameFrame = Frame(self.master)
		self.gameFrame.pack()

		# creating labels
		self.mineLabels = []
		for i in range(N):
			for j in range(M):
				tile = j+i*M
				self.mineLabels.append(Label(self.gameFrame, text = '%d' % tile,
					image = self.getImage(tile), borderwidth = 1, relief = "solid"))
				self.mineLabels[tile].grid(row = i+2, column = j)
				self.mineLabels[tile].bind('<1>', self.right_click)
				self.mineLabels[tile].bind('<2>', self.left_click)
				self.mineLabels[tile].bind('<3>', self.left_click)
	
		# creating frame to store info other than the game grid
		self.infoFrame = Frame(self.master)
		self.infoFrame.pack()
	
		# remaining mines label
		self.minesLabel = Label(self.infoFrame, text = self.minesMessage % numMines)
		self.minesLabel.pack()
		
		# elapsed time label
		self.timeLabel = Label(self.infoFrame, text = '0 second(s)')
		self.timeLabel.pack()

		self.updateElapsedTime()

	def updateElapsedTime(self):
		if self.game.gameState == 0:
			self.startTime = time.time()
			self.master.after(10, self.updateElapsedTime)
			return
		
		if self.game.gameState == 2:
			return

		newText = str(int(time.time() - self.startTime)) + ' second(s)'
		self.timeLabel.text = newText 
		self.timeLabel.configure(text = newText)
		self.master.after(500, self.updateElapsedTime)

	def newGamePopup(self):
		self.popup = Toplevel()
		
		# options to create a new game
		self.sizeLabel = Label(self.popup, text = 'Size: ')
		self.sizeLabel.pack(side = LEFT)
		
		self.nField = Entry(self.popup, width = 3)
		self.nField.insert(0, str(self.game.N))
		self.nField.pack(side = LEFT)
		
		self.mField = Entry(self.popup, width = 3)
		self.mField.insert(0, str(self.game.M))
		self.mField.pack(side = LEFT)
		
		self.numMinesLabel = Label(self.popup, text = 'Number of mines: ')
		self.numMinesLabel.pack(side = LEFT)
		
		self.minesField = Entry(self.popup, width = 3)
		self.minesField.insert(0, str(self.game.numMines))
		self.minesField.pack(side = LEFT)
		
		newGameFunction = lambda: self.generate(int(self.nField.get()), int(self.mField.get()), int(self.minesField.get()))
		self.newGameButton = Button(self.popup, text = 'Create Game', command = newGameFunction)
		self.newGameButton.pack()

def main():
	root = Tk()
	root.title("Minesweeper")
	minesweeper = Minesweeper(root)
	root.resizable(False, False)

	# menu
	menubar = Menu(root)
	menubar.add_command(label = 'New Game', command = minesweeper.newGamePopup)
	root.config(menu = menubar)
	
	root.mainloop()

if __name__ == "__main__":
	main()
