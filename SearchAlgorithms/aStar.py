import queue, os, pygame, ctypes, random
from time import time
screen_size = [1300, 700]

#Classes
class Node:
	def __init__(self, x, y, w, h, row, col, state):
		self.rect = pygame.Rect(x, y, w, h)
		self.state = state
		self.row = row
		self.col = col
		self.f = 0
		self.g = 0
		self.h = 0
		self.neighbours = []
		self.previous = None

	def change_state(self, new_state):
		self.state = new_state

	def calc_h_val(self, game):
		self.h = abs(self.row-game.end_row) + abs(self.col-game.end_col)

	def add_neighbours(self, nodes):
		if self.row != 0:
			self.neighbours.append(nodes[self.row-1][self.col])
		if self.col != 0:
			self.neighbours.append(nodes[self.row][self.col-1])
		if self.row != len(nodes)-1:
			self.neighbours.append(nodes[self.row+1][self.col])
		if self.col != len(nodes[0])-1:
			self.neighbours.append(nodes[self.row][self.col+1])

	def path_found(self):
		if self.state != "start" and self.state != "end":
			self.change_state("found")
		if self.previous != None:
			self.previous.path_found()	

	def draw(self):
		if self.state == "wall":
			pygame.draw.rect(Screen, (0, 0, 0), self.rect)
		elif self.state == "unexplored":
			pygame.draw.rect(Screen, (200, 200, 200), self.rect)
		elif self.state == "explored":
			pygame.draw.rect(Screen, (100, 100, 100), self.rect)
		elif self.state == "found":
			pygame.draw.rect(Screen, (128, 0, 128), self.rect)
		elif self.state == "start":
			pygame.draw.rect(Screen, (0, 255, 0), self.rect)
		elif self.state == "end":
			pygame.draw.rect(Screen, (255, 0, 0), self.rect)
		pygame.draw.rect(Screen, (127, 127, 127), self.rect, 2)


class Game:
	def __init__(self):
		self.left_pressed = False
		self.right_pressed = False

		self.has_started = False
		self.has_start = False
		self.has_end = False
		self.has_ended = False


#Methods
def create_nodes(screen_width, screen_height, node_size):
	nodes = []
	for i in range(screen_height//node_size):
		row_of_nodes = []
		for j in range(screen_width//node_size):
			if i == 0 or i == (screen_height//node_size-1) or j == 0 or j == (screen_width//node_size-1):
				row_of_nodes.append(Node(j*node_size, i*node_size, node_size, node_size, i, j, "wall"))
			else:
				row_of_nodes.append(Node(j*node_size, i*node_size, node_size, node_size, i, j, "unexplored"))
		nodes.append(row_of_nodes)
	return nodes

def get_row_and_col(mouse_pos, node_size):
	col = mouse_pos[0]//node_size
	row = mouse_pos[1]//node_size
	return [row, col]

def get_row(mouse_pos, node_size):
	return mouse_pos[1]//node_size

def get_col(mouse_pos, node_size):
	return mouse_pos[0]//node_size

def get_node(order, nodes, start_row, start_col):
	end_row = start_row + order.count("D") - order.count("U")
	end_col = start_col + order.count("R") - order.count("L")

	return nodes[end_row][end_col]

#General variables
pygame.init()
Screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("aStar")
FRAMERATE = 10
node_size = 20

#Objects
q = queue.PriorityQueue()
nodes = create_nodes(screen_size[0], screen_size[1], node_size)
for row in nodes:
	for node in row:
		node.add_neighbours(nodes)
game = Game()


run = True
while run:
	#Events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		elif event.type == pygame.KEYDOWN:
			if event.key == 27:
				run = False
	
	if game.has_started and not game.has_ended:
		if q.qsize() != 0:
			current = q.get()[1]
			if current.state == "end":
				game.has_ended = True
			if not game.has_ended:
				for node in current.neighbours:
					if node.state == "unexplored" or node.state == "end":
						if node.state == "unexplored":
							nodes[node.row][node.col].change_state("explored")
						node.previous = current
						node.g = current.g + 1
						node.f = node.g + node.h + random.random()/100
						q.put((node.f, node))
		else:
			game.has_ended = True
			print("NO WAY TO GET TO GOAL")
	elif not game.has_started:
		#Set walls
		m = pygame.mouse.get_pressed()
		if m[0]:
			game.left_pressed = True
			m_pos = pygame.mouse.get_pos()
			row, col = get_row_and_col(m_pos, node_size)
			if nodes[row][col].state == "unexplored":
				nodes[row][col].change_state("wall")
		elif not m[0]:
			game.left_pressed = False
	
		#Set start and end and begin
		if m[2] and not game.right_pressed:
			game.right_pressed = True
			m_pos = pygame.mouse.get_pos()
			if not game.has_start:
				if nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].state == "unexplored":
					nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].change_state("start")
					game.has_start = True
					game.start_row = get_row(m_pos, node_size)
					game.start_col = get_col(m_pos, node_size)
			elif not game.has_end:
				if nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].state == "unexplored":
					nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].change_state("end")
					game.has_end = True
					game.end_row = get_row(m_pos, node_size)
					game.end_col = get_col(m_pos, node_size)
			else:
				game.has_started = True
		elif not m[2]:
			game.right_pressed = False
		if game.has_started:
			for row in nodes:
				for node in row:
					node.calc_h_val(game)
			q.put((nodes[game.start_row][game.start_col].f, nodes[game.start_row][game.start_col]))
			t1 = time()
	else:
		nodes[game.end_row][game.end_col].path_found()
	
	#Draw
	for row in nodes:
		for node in row:
			node.draw()
	
	pygame.display.update()
	#pygame.time.delay(1000//FRAMERATE)
	