import pygame, ctypes, os

#Classes
class Node:
	def __init__(self, x, y, w, h, row, col):
		self.rect = pygame.Rect(x, y, w, h)
		self.black = False
		self.next_black = False
		self.row = row
		self.col = col

	def draw(self):
		if self.black:
			pygame.draw.rect(Screen, (0, 0, 0), self.rect)
		else:
			pygame.draw.rect(Screen, (255, 255, 255), self.rect)
		pygame.draw.rect(Screen, (127, 127, 127), self.rect, 2)

	def clicked(self):
		self.black = True

	def calc_next_black(self, nodes):
		live_around = 0
		for i in range(-1, 2):
			for j in range(-1, 2):
				if i != 0 or j != 0:
					live_around += nodes[row+i][col+j].black
		if self.black:
			if live_around == 2 or live_around == 3:
				self.next_black = True
			else:
				self.next_black = False
		else:
			if live_around == 3:
				self.next_black = True
			else:
				self.next_black = False

	def change_black(self):
		self.black = self.next_black


#Methods
def create_nodes():
	nodes = []
	for i in range(screen_height//node_size):
		row_of_nodes = []
		for j in range(screen_width//node_size):
			row_of_nodes.append(Node(j*node_size, i*node_size, node_size, node_size, i, j))
		nodes.append(row_of_nodes)
	return nodes


pygame.init()
screen_width = 1000
screen_height = 500
node_size = 20
has_started = False
Screen = pygame.display.set_mode((screen_width, screen_height))
nodes = create_nodes()

run = True
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.KEYDOWN:
			if event.key == 27:
				run == False

	#Draw
	Screen.fill((255, 255, 0))
	for row in nodes:
		for node in row:
			node.draw()
	
	#Mouse
	m = pygame.mouse.get_pressed()
	if m[0] and not has_started:
		m_pos = pygame.mouse.get_pos()
		nodes[m_pos[1]//node_size][m_pos[0]//node_size].clicked()
	elif m[0] and has_started:
		has_started = False
	elif m[2] and not has_started:
		has_started = True


	pygame.display.update()
	
	if has_started:
		for row in range(1, len(nodes)-1):
			for col in range(1, len(nodes[row])-1):
				nodes[row][col].calc_next_black(nodes)
		for row in range(1, len(nodes)-1):
			for col in range(1, len(nodes[row])-1):
				nodes[row][col].change_black()
		pygame.time.delay(1000//10)
	else:
		pygame.time.delay(1000//60)

