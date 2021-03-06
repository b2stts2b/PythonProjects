import pygame
pygame.init()

class Board:
	def __init__(self):
		self.board = self.create_board()

		self.player_one = True
		self.is_click = False

	def create_board(self):
		board = []
		for _ in range(3):
			row = []
			for _ in range(3):
				row.append("")
			board.append(row)
		return board

	def draw_board(self):
		for x in range(50, (s_w-50+1), (s_w-100)//3):
			pygame.draw.line(Screen, 0, (x, 50), (x, (s_h-50)), 5)
		for y in range(50, (s_w-50+1), (s_w-100)//3):
			pygame.draw.line(Screen, 0, (50, y), ((s_h-50), y), 5)

		for x in range(3):
			for y in range(3):
				if self.board[y][x] == "X":
					pygame.draw.line(Screen, 0, (65+x*(500//3), 65+y*(500//3)), (35+(x+1)*(500//3), 35+(y+1)*(500//3)),20)
					pygame.draw.line(Screen, 0, (65+x*(500//3), 35+(y+1)*(500//3)), (35+(x+1)*(500//3), 65+y*(500//3)),20)
				elif self.board[y][x] == "O":
					pygame.draw.circle(Screen, 0, (50+500//6+x*(500//3),50+500//6+y*(500//3)), 500//7)

	def board_clicked(self, pos):
		x_i = (pos[0]-50)//(500//3)
		y_i = (pos[1]-50)//(500//3)
		if x_i in [0,1,2] and y_i in [0,1,2]:
			if self.board[y_i][x_i] == "":
				self.board[y_i][x_i] = "X" if self.player_one else "O"
				self.player_one = not self.player_one
				self.check_win()

	def check_win(self):
		if self.board[0][0] == self.board[1][1] and self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
				print("You won!")
		if self.board[2][0] == self.board[1][1] and self.board[1][1] == self.board[0][2] and self.board[2][0] != "":
				print("You won!")
		for r,val in enumerate(self.board):
			if len(set(val)) == 1 and val[0] != "":
				print("You won!")
			if self.board[0][r] == self.board[1][r] and self.board[2][r] == self.board[1][r] and self.board[0][r] != "":
				print("You won!")


s_w, s_h = 600, 600
Screen = pygame.display.set_mode((s_w, s_h))
board = Board()

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == 27:
				run = False


	m = pygame.mouse.get_pressed()
	if m[0] and not board.is_click:
		#we clicked
		board.is_click = True
		board.board_clicked(pygame.mouse.get_pos())
	elif not m[0] and board.is_click:
		#we stop click
		board.is_click = False

	Screen.fill((150, 150, 150))
	board.draw_board()

	pygame.display.update()