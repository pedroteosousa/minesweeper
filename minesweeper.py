from Tkinter import *
from numpy import *

class Minesweeper:
	def __init__(self, master):
		self.master = master
	
		# loading images
		self.tile_img = PhotoImage(file = "images/tile.gif")
		self.bomb_img = PhotoImage(file = "images/bomb.gif")

		# generating a game for testing
		self.generate(15, 10, 50)
	
	# events that handle clicking on a tile
	def right_click(self, event):
		pos = event.widget.cget('text').split()
		print(pos)
	
	def generate(self, N, M, num_mines):
		try:
			self.frame.destroy()
		except AttributeError:
			print("could not destroy current frame")
			
		self.frame = Frame(self.master)
		self.frame.pack()
	
		# creating game grid (-1 for mines 0 for empty and any other value represent number of adjacent mines)
		self.mines = [[0] * M for j in range(N)]
		mine_locations = random.permutation(N * M)[0:num_mines]
		for mine in mine_locations:
			self.mines[mine % N][mine // N] = -1
	
		# creating labels
		self.mine_labels = []
		for i in range(N):
			self.mine_labels.append([])
			for j in range(M):
				# choose image to put on tile
				img = self.tile_img
				if self.mines[i][j] == -1:
					img = self.bomb_img
				
				self.mine_labels[i].append(Label(self.frame, text='%d %d' % (i, j), image=img, borderwidth=1))
				self.mine_labels[i][j].grid(row=j, column=i)
				self.mine_labels[i][j].bind('<1>', self.right_click)
				
def main():
    root = Tk()
    root.title("Minesweeper")
    minesweeper = Minesweeper(root)
    root.resizable(False, False)
    root.mainloop()

if __name__ == "__main__":
    main()

