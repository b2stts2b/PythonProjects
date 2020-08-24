import queue, os, pygame, ctypes

os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 0)
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
screen_size = [600, 400]

#Classes
class Node:
	def __init__(self, x, y, w, h, row, col, state):
		self.rect = pygame.Rect(x, y, w, h)
		self.state = state
		self.row = row
		self.col = col

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

	def change_state(self, new_state):
		self.state = new_state

class Game:
	def __init__(self):
		self.left_pressed = False
		self.right_pressed = False

		self.has_started = False
		self.has_start = False
		self.has_end = False

		self.start_row = 0
		self.start_col = 0

		self.found_path = False
		self.path = ""

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

def going_back(d1, d2):
	if len(d1) == 0:
		return False
	if d1[-1] == "U" and d2 == "D":
		return True
	elif d1[-1] == "D" and d2 == "U":
		return True
	elif d1[-1] == "R" and d2 == "L":
		return True
	elif d1[-1] == "L" and d2 == "R":
		return True
	return False

def change_states(row, col, nodes, path):
	for d in path:
		if d == "U":
			row -= 1
		elif d == "R":
			col += 1
		elif d == "D":
			row += 1
		elif d == "L":
			col -= 1
		nodes[row][col].change_state("found")

#General variables
pygame.init()
Screen = pygame.display.set_mode(screen_size)
FRAMERATE = 30
node_size = 20

#Objects
q = queue.Queue()
q.put("")
nodes = create_nodes(screen_size[0], screen_size[1], node_size)
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
	
	#Set walls
	m = pygame.mouse.get_pressed()
	if m[0] and not game.has_started:
		game.left_pressed = True
		m_pos = pygame.mouse.get_pos()
		row, col = get_row_and_col(m_pos, node_size)
		nodes[row][col].change_state("wall")
	elif not m[0]:
		game.left_pressed = False
	
	#Set start and end and begin
	if m[2] and not game.has_started and not game.right_pressed:
		game.right_pressed = True
		m_pos = pygame.mouse.get_pos()
		if not game.has_start:
			if nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].state == "unexplored":
				nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].change_state("start")
				game.start_row = get_row(m_pos, node_size)
				game.start_col = get_col(m_pos, node_size)
				game.has_start = True
		elif not game.has_end:
			if nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].state == "unexplored":
				nodes[get_row(m_pos, node_size)][get_col(m_pos, node_size)].change_state("end")
				game.has_end = True
		else:
			game.has_started = True
	elif not m[2]:
		game.right_pressed = False
	
	#Go through one iteration of queue
	if not game.found_path and game.has_started:
		next_order = q.get()
		for direction in ["U", "R", "D", "L"]:
			if not going_back(next_order, direction):
				modified_order = next_order + direction
				node = get_node(modified_order, nodes, game.start_row, game.start_col)
				if node.state == "unexplored":
					node.change_state("explored")
					q.put(modified_order)
				elif node.state == "end":
					game.found_path = True
					game.path = next_order
					change_states(game.start_row, game.start_col, nodes, game.path)
					break
	
	#Draw
	for row in nodes:
		for node in row:
			node.draw()
	
	pygame.display.update()
	#pygame.time.delay(1000//FRAMERATE)
	