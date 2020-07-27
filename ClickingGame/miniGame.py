import pygame, os, ctypes
import pygame.freetype
from random import randint
from math import sqrt
from time import time

"""
	TODO:
	-	Upload Leaderboard to external textFile
"""

#General Things
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (0, 0)
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1) 
screen_width, screen_height = screensize
FRAMERATE = 60
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
pygame.init()

#Fonts
buttonFont = pygame.freetype.SysFont("Arial", 20)
timeFont = pygame.freetype.SysFont("Arial", 30)
scoreFont = pygame.freetype.SysFont("Arial", 50)
endFont = pygame.freetype.SysFont("comicsansms", 70)
endTimeFont = pygame.freetype.SysFont("comicsansms", 30)
nameFont = pygame.freetype.SysFont("Arial", 90)
LeaderboardFonts = {"1":pygame.freetype.SysFont("Georgia", 30), 
					"2":pygame.freetype.SysFont("Georgia", 50), 
					"3":pygame.freetype.SysFont("Georgia", 60)}


def main():
	#Classes
	class Button:
		def __init__(self, text, pos, function):
			self.text = text
			self.function = function
			self.rect = pygame.Rect(0, 0, 200, 50)
			self.rect.center = pos
			self.text, self.text_rect = buttonFont.render(function, (255, 255, 255))
			self.text_rect.center = pos
		def draw(self):
			pygame.draw.rect(Screen, (255, 255, 255), self.rect, 4)
			Screen.blit(self.text, self.text_rect)

		def mouseInside(self, mousePos):
			if self.rect.left <= mousePos[0] and  self.rect.right >= mousePos[0] and self.rect.top <= mousePos[1] and self.rect.bottom >= mousePos[1]:
				return True
			return False


	class Mouse:
		def __init__(self):
			self.isPressed = False	

	#Methods
	def addButtons():
		buttons = []
		buttons.append(Button("clickingGame", [screen_width//2, screen_height//4], "clickingGame"))
		buttons.append(Button("Leaderboard", [screen_width//2, screen_height//2], "Leaderboard"))
		buttons.append(Button("QUIT", [screen_width//2, screen_height*3//4], "QUIT"))
		return buttons	


	#General Things
	Screen = pygame.display.set_mode(screensize)
	pygame.mixer.music.load("music/song.mp3")
	pygame.mixer.music.play(-1)	
	pygame.mixer.music.set_volume(0.25)

	#Objects
	buttons = addButtons()
	mouse = Mouse()

	run = True
	while run:
		#Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == 27:
					run = False


		#Get mousePresses
		m = pygame.mouse.get_pressed()
		if m[0]:
			mouse.isPressed = True
		elif not m[0] and mouse.isPressed:
			#We released leftClick
			mouse.isPressed = False
			mousePos = pygame.mouse.get_pos()
			for button in buttons:
				if button.mouseInside(mousePos):
					if button.function == "QUIT":
						run = False
						break
					elif button.function == "clickingGame":
						chooseClickingGame()
						break
					elif button.function == "Leaderboard":
						Leaderboard()
						break
						


		Screen.fill((25, 25, 25))


		#Draw stuff
		for button in buttons:
			button.draw()

		#End of Fram
		pygame.display.update()
		pygame.time.delay(1000//FRAMERATE)

def chooseClickingGame():
	#Classes
	class Button:
		def __init__(self, text, pos, function):
			self.text = text
			self.function = function
			self.rect = pygame.Rect(0, 0, 200, 50)
			self.rect.center = pos
			self.text, self.text_rect = buttonFont.render(function, (255, 255, 255))
			self.text_rect.center = pos
		def draw(self):
			pygame.draw.rect(Screen, (255, 255, 255), self.rect, 4)
			Screen.blit(self.text, self.text_rect)

		def mouseInside(self, mousePos):
			if self.rect.left <= mousePos[0] and  self.rect.right >= mousePos[0] and self.rect.top <= mousePos[1] and self.rect.bottom >= mousePos[1]:
				return True
			return False


	class Mouse:
		def __init__(self):
			self.isPressed = False	

	#Methods
	def addButtons():
		buttons = []
		buttons.append(Button("Easy", [screen_width//2, screen_height//4], "Easy"))
		buttons.append(Button("Medium", [screen_width//2, screen_height//2], "Medium"))
		buttons.append(Button("Hard", [screen_width//2, screen_height*3//4], "Hard"))
		return buttons	

	#General Things
	Screen = pygame.display.set_mode(screensize)

	#Objects
	buttons = addButtons()
	mouse = Mouse()

	run = True
	while run:
		#Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == 27:
					run = False

		#Draw stuff
		Screen.fill((25, 25, 25))
		for button in buttons:
			button.draw()

		#End of Fram
		pygame.display.update()
		pygame.time.delay(1000//FRAMERATE)


		#Get mousePresses
		m = pygame.mouse.get_pressed()
		if m[0]:
			mouse.isPressed = True
		elif not m[0] and mouse.isPressed:
			#We released leftClick
			mouse.isPressed = False
			mousePos = pygame.mouse.get_pos()
			for button in buttons:
				if button.mouseInside(mousePos):
					if button.function == "Easy":
						clickingGame(30, 10, "Easy")
					elif button.function == "Medium":
						clickingGame(20, 10, "Medium")
					elif button.function == "Hard":
						clickingGame(10, 10, "Hard")
					run = False

def clickingGame(size, times, difficulty):
	#Classes
	class Circle():
		def __init__(self, rad, timesLeft, color, pos):
			self.pos = pos
			self.rad = rad
			self.color = color
			self.timesLeft = timesLeft

		def draw(self):
			pygame.draw.circle(Screen, self.color, self.pos, self.rad)

		def isClicked(self, mousePos):
			return (sqrt((self.pos[0]-mousePos[0])**2+(self.pos[1]-mousePos[1])**2) <= self.rad)

		def changePos(self):
			self.pos = [randint(self.rad, screen_width-self.rad), randint(self.rad, screen_height-self.rad)]


	class NameButton:
		def __init__(self, pos, rad):
			self.pos = pos
			self.rad = rad
			self.val = 0
			self.text, self.rect = nameFont.render("A", (255, 255, 255))
			self.rect.center = pos

		def draw(self):
			Screen.blit(self.text, self.rect)
			pygame.draw.circle(Screen, (255, 255, 255), [self.pos[0], self.pos[1]-100], self.rad)
			pygame.draw.circle(Screen, (255, 255, 255), [self.pos[0], self.pos[1]+100], self.rad)

		def clicked(self, m_pos):
			if sqrt((m_pos[0]-self.pos[0])**2+(m_pos[1]-(self.pos[1]-100))**2) < self.rad:
				self.val = (self.val-1)%len(LETTERS)
				self.text, self.rect = nameFont.render(LETTERS[self.val], (255, 255, 255))
				self.rect.center = self.pos
			if sqrt((m_pos[0]-self.pos[0])**2+(m_pos[1]-(self.pos[1]+100))**2) < self.rad:
				self.val = (self.val+1)%len(LETTERS)
				self.text, self.rect = nameFont.render(LETTERS[self.val], (255, 255, 255))
				self.rect.center = self.pos


	class Mouse:
		def __init__(self):
			self.isPressed = False	


	class Button:
		def __init__(self, pos, w, h):
			self.rect = pygame.Rect(0, 0, w, h)
			self.rect.center = pos

		def draw(self):
			pygame.draw.rect(Screen, (255, 255, 255), self.rect, 4)

		def isClicked(self, mouse_pos):
			return (mouse_pos[0] > self.rect.left and mouse_pos[0] < self.rect.right and mouse_pos[1] < self.rect.bottom and mouse_pos[1] > self.rect.top)

	#Methods
	def addNames():
		names = []
		for i in range(3):
			names.append(NameButton([screen_width//2-100+100*i, 3*screen_height//5], 30))
		return names

	def load_highscore(diff):
		if diff == "Easy":
			with open("text/miniGameLeaderboardEasy.txt") as f:
				highscore = []
				scores = f.read().split("\n")
				for i, val in enumerate(scores):
					name, score = val.split(",")
					highscore.append([name, float(score)])
		elif diff == "Medium":
			with open("text/miniGameLeaderboardMedium.txt") as f:
				highscore = []
				scores = f.read().split("\n")
				for i, val in enumerate(scores):
					name, score = val.split(",")
					highscore.append([name, float(score)])
		elif diff == "Hard":
			with open("text/miniGameLeaderboardHard.txt") as f:
				highscore = []
				scores = f.read().split("\n")
				for i, val in enumerate(scores):
					name, score = val.split(",")
					highscore.append([name, float(score)])
		return highscore

	def upload_highscore(highscore, diff):
		new_highscore = []
		for h in highscore:
			name = h[0]
			val = str(h[1])
			new_highscore.append(f"{name},{val}")
		with open(f"text/miniGameLeaderboard{diff}.txt", "w") as f:
			f.write("\n".join(high for high in new_highscore))


	#General Things
	Screen = pygame.display.set_mode(screensize)
	timer = 0
	highscore = load_highscore(difficulty)
	
	#Objects
	circle = Circle(size, times, (255, 0, 0), [screen_width//2, screen_height//2])
	mouse = Mouse()

	run = True
	while run:
		t1 = time()
		
		#Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == 27:
					run = False

		#Get input from mouse
		m = pygame.mouse.get_pressed()
		if m[0]:
			mouse.isPressed = True
		elif not m[0] and mouse.isPressed:
			mouse.isPressed = False
			if circle.isClicked(pygame.mouse.get_pos()):
				circle.timesLeft -= 1
				circle.changePos()
				if circle.timesLeft <= 0:
					run = False

		if run:		
			#Draw
			Screen.fill((0,0,0))
			circle.draw()

			#Texts
			scoreText, scoreTextRect = scoreFont.render(f"Left: {circle.timesLeft}", (255,255,255))
			scoreTextRect.center = (screen_width//2, screen_height//20)
			timeText, timeTextRect = timeFont.render(f"Time: {round(timer, 2)}", (255, 255, 255))
			timeTextRect.right = screen_width-10
			timeTextRect.top = 10

			#Blit text
			Screen.blit(scoreText, scoreTextRect)
			Screen.blit(timeText, timeTextRect)

			#End of frame
			pygame.display.update()
			pygame.time.delay(1000//FRAMERATE)
			timer += time()-t1

		else:
			timer += time()-t1
			#Draw
			Screen.fill((50,50,50))

			
			if circle.timesLeft <= 0:
				#Text
				gameOverText, gameOverTextRect = endFont.render("GAME OVER", (255, 255, 255))
				gameOverTextRect.center = (screen_width//2, screen_height//6)
				timeText, timeTextRect = endTimeFont.render(f"Time: {round(timer, 4)}s", (255, 255, 255))
				timeTextRect.midtop = (screen_width//2, gameOverTextRect.bottom+20)
				no_highscore_text, no_highscore_rect = endFont.render("HIGH SCORE!", (255, 255, 255))
				no_highscore_rect.midtop = (timeTextRect.centerx, timeTextRect.bottom+40)
				

				button = Button((screen_width//2, 6*screen_height//7), 200, 50)

				if timer < highscore[-1][1]:
					names = addNames()
					run_2nd = True
					while run_2nd:
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								run_2nd = False
							elif event.type == pygame.KEYDOWN:
								if event.key == 27:
									run_2nd = False

						Screen.fill((50, 50, 50))
						
						Screen.blit(gameOverText, gameOverTextRect)
						Screen.blit(timeText, timeTextRect)
						Screen.blit(no_highscore_text, no_highscore_rect)


						for name in names:
							name.draw()
						button.draw()

						#Get input from mouse
						m = pygame.mouse.get_pressed()
						m_pos = pygame.mouse.get_pos()
						if m[0]:
							mouse.isPressed = True
						elif not m[0] and mouse.isPressed:
							mouse.isPressed = False
							if button.isClicked(m_pos):
								run_2nd = False
								highscore.append(["".join(LETTERS[name.val] for name in names), round(timer, 4)])
								highscore.sort(key = lambda x: x[1])
								highscore.pop(-1)
								upload_highscore(highscore, difficulty)
							for name in names:
								name.clicked(m_pos)

						pygame.display.update()
						pygame.time.delay(1000//FRAMERATE)


				else:
					#We did not hit highscore
					no_highscore_text, no_highscore_rect = endFont.render("No highscore:(", (255, 255, 255))
					no_highscore_rect.midtop = (timeTextRect.centerx, timeTextRect.bottom+50)
					Screen.blit(no_highscore_text, no_highscore_rect)
					
					#Blit text
					Screen.blit(gameOverText, gameOverTextRect)
					Screen.blit(timeText, timeTextRect)
			
					#End of frame
					pygame.display.update()
					pygame.time.delay(4000)

def Leaderboard():
	#Classes
	class textObject:
		def __init__(self, text, color, font, pos = (0, 0)):
			self.text, self.rect = LeaderboardFonts[font].render(text, color)
			self.rect.center = pos

	#Methods
	def get_default_text():
		texts = []
		texts.append(textObject("HIGH SCORES", (255, 255, 255), "3"))
		texts.append(textObject("Easy", (255, 255, 255), "2"))
		texts.append(textObject("Medium", (255, 255, 255), "2"))
		texts.append(textObject("Hard", (255, 255, 255), "2"))

		texts[0].rect.midtop = (screen_width//2, 20)
		texts[1].rect.midtop = (screen_width//6, texts[0].rect.bottom+20)
		texts[2].rect.midtop = (screen_width//2, texts[0].rect.bottom+20)
		texts[3].rect.midtop = ((5*screen_width)//6, texts[0].rect.bottom+20)

		return texts

	def LoadLeaderboard(texts):
		#LOAD EASY SCORES
		with open("text/miniGameLeaderboardEasy.txt", "r") as f:
			scores = f.read().split("\n")
			for i, val in enumerate(scores):
				name, score = val.split(",")
				texts.append(textObject(f"{i+1}. {name} {score}", (255, 255, 255), "1", (texts[1].rect.centerx, texts[1].rect.centery+(i+1)*50)))

		#LOAD EASY SCORES
		with open("text/miniGameLeaderboardMedium.txt", "r") as f:
			scores = f.read().split("\n")
			for i, val in enumerate(scores):
				name, score = val.split(",")
				texts.append(textObject(f"{i+1}. {name} {score}", (255, 255, 255), "1", (texts[2].rect.centerx, texts[2].rect.centery+(i+1)*50)))
		
		#LOAD EASY SCORES
		with open("text/miniGameLeaderboardHard.txt", "r") as f:
			scores = f.read().split("\n")
			for i, val in enumerate(scores):
				name, score = val.split(",")
				texts.append(textObject(f"{i+1}. {name} {score}", (255, 255, 255), "1", (texts[3].rect.centerx, texts[3].rect.centery+(i+1)*50)))


	#General
	Screen = pygame.display.set_mode(screensize)

	#Texts
	texts = get_default_text()
	LoadLeaderboard(texts)


	run = True
	while run:
		#Events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == 27:
					run = False



		#Blit Text
		for text in texts:
			Screen.blit(text.text, text.rect)



		pygame.display.update()
		pygame.time.delay(1000//FRAMERATE)

main()