class ThisAintItError(Exception):
	pass

class Sudoku:
	def __init__(self, board=None):
		if board is None:
			self.board = [[None] * 9] * 9
		else:
			self.parse(board)
		self.guessSwitch = False
		
	def parse(self, board):
		board = board.split('\n')
		
		def process_char(c):
			try:
				if int(c) in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
					return int(c)
				else:
					return None
			except:
				return None

		self.board = []

		for line in board:
			self.board.append([process_char(c) for c in line])

	def __repr__(self):
		out_string = ""
		out_string += "┏━━━┯━━━┯━━━┳━━━┯━━━┯━━━┳━━━┯━━━┯━━━┓\n"
		j = 1
		for line in self.board:
			h = 1
			for c in line:
				if c is not None:
					if h % 3 == 1:
						out_string += "┃ "
						out_string += str(c)
						out_string += " "
					else:
						out_string += "│ "
						out_string += str(c)
						out_string += " "
				else:
					if h % 3 == 1:
						out_string += "┃   " 
					else:
						out_string +="│   "
				h += 1
			out_string += "┃ \n"
			if line != self.board[8]:
				if j % 3 == 0:
					out_string += "┣━━━┿━━━┿━━━╋━━━┿━━━┿━━━╋━━━┿━━━┿━━━┫ \n"
				else:	
					out_string += "┠───┼───┼───╂───┼───┼───╂───┼───┼───┨ \n"
			else:
				out_string += "┗━━━┷━━━┷━━━┻━━━┷━━━┷━━━┻━━━┷━━━┷━━━┛ \n"
			j += 1
			
		return out_string

	#def collumns(self):
		#self.collumns = [[],[],[],[],[],[],[],[],[]]
		#for line in self.board:
			#for i in range(len(line)):
				#self.collumns[i].append(line[i])
		#print(self.collumns)

	#def boxes(self):
		#self.boxes = [{},{},{},{},{},{},{},{},{}]
		
	#def possibile_solutions(self,i,e):
		#pass

	def poss(self,i,j):
		if self.board[j][i] is None:
			pass_digits = {1,2,3,4,5,6,7,8,9}
			pass_digits -= set(self.board[j])
			pass_digits -= set([self.board[k][i] for k in range(9)])

			box_i = 3*(i//3)
			box_j = 3*(j//3)

			for k in range(3):
				pass_digits -= set(self.board[box_j + k][box_i:box_i+3])

			return pass_digits
		else:
			return {self.board[j][i]}
			
	def reduce_one_pass(self):
		for i in range(9):
			for j in range(9):
				if self.board[j][i] is None:
					square_poss = self.poss(i,j)
					if len(square_poss) == 1:
						self.board[j][i] = list(square_poss)[0]
						self.changed = True
					

	def reduce_row_poss(self):
		for i in range(9):
			row_poss = [self.poss(i, j) for j in range(9)]
			for digit in range(1,10):
				pass_cells = [k for k,square in enumerate(row_poss) if digit in square]
				if len(pass_cells) == 1 and self.board[pass_cells[0]][i] == None:
					self.board[pass_cells[0]][i] = digit
					self.changed = True
				

	def reduce_col_poss(self):
		for i in range(9):
			col_poss = [self.poss(j,i) for j in range(9)]
			for digit in range(1,10):
				pass_cells = [k for k,square in enumerate(col_poss) if digit in square]
				if len(pass_cells) == 1 and self.board[i][pass_cells[0]] == None:
					self.board[i][pass_cells[0]] = digit
					self.changed = True
				
				

	

	def guess(self):
		backupBoard = self.board
		for i in range(9):
			for j in range(9):
				if self.board[j][i] is None:
					square_poss = list(self.poss(i,j))
					if len(square_poss) == 2 and self.board[j][i] == None:
						try:
							self.board[j][i] = square_poss[0]
							print("guess")
							self.solve()
						except ThisAintItError:
							print("Shift")
							self.board = backupBoard
							self.board[j][i] = square_poss[1]
							self.changed = True
							return
		self.changed2 = False			


	def validityCheck(self):
		for i in range(9):
			for j in range(9):
				if self.board[j][i] is None:
					square_poss = list(self.poss(i,j))
					print(square_poss)
					if len(square_poss) == 0:
						raise ThisAintItError()
						print("ShiftCheck")
		
		

	
	def solve(self):
		while True:
			self.changed = False
			self.reduce_one_pass()
			self.reduce_row_poss()
			self.reduce_col_poss()
			self.validityCheck
			self.guess()
			
			
			print(self)
			if not self.changed:
				print(self)
				break
		
		
def main():
	board = "3....2...\n2.8..7...\n...514...\n...1...7..\n69.....8.\n....9...2\n.2....4.5\n..5......\n..4.7.1.."
	testBoard = Sudoku(board)
	print(testBoard)
	testBoard.solve()
main()
