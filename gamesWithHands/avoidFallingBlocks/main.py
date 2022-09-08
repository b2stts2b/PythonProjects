import pygame as pg
import numpy as np
import cv2 
import mediapipe as mp
from threading import Thread
import random
import time

# Player class
class Player(Thread):
	def __init__(self, size = 10, draw = False):
		Thread.__init__(self)
		self.w = 640
		self.h = 480
		self.x = 0
		self.y = 0
		self.size = size
		self.running = True
		self.draw = draw
		self.rect = pg.Rect(self.x, self.y, self.size, self.size)

	def get_coord(self):
		return self.rect.center

	def get_direction(self, x_pos, y_pos):
		"""Return normalized vector from (x_pos, y_pos) to self.rect"""
		vector = np.array([self.rect.x-x_pos, self.rect.y-y_pos])
		return vector/np.linalg.norm(vector)

	def check_collision(self, enemy_rect):
		return self.rect.colliderect(enemy_rect)

	def run(self):
		# create camera capture
		cap = cv2.VideoCapture(0)
		self.w = cap.get(3)
		self.h = cap.get(4)

		# Class for finding hands,
		with mp_hands.Hands(
			max_num_hands=1,
			model_complexity=0,
			min_detection_confidence=0.8,
			min_tracking_confidence=0.8) as hands:
			
			# Track hands while camera is open
			while cap.isOpened() and self.running:
				success, image = cap.read()
				if not success:
					continue

				# Improve performance and find hands
				image.flags.writeable = False
				image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
				result = hands.process(image)

				# Revert changes
				image.flags.writeable = False
				image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

				# Draw hand annotations on image
				if result.multi_hand_landmarks:
					for hand_landmarks in result.multi_hand_landmarks:
						# Use position of index finger
						self.x = 1-hand_landmarks.landmark[8].x
						self.y = hand_landmarks.landmark[8].y
						self.rect = pg.Rect(self.x*self.w, self.y*self.h, self.size, self.size)

				# Show flipped image
				if self.draw:
					image = cv2.circle(image, self.get_coord(), 20, (0, 255, 0), 3)
					cv2.imshow("Hands", cv2.flip(image, 1))
				if cv2.waitKey(5) & 0xFF == ord("q"):
					self.running = False

# Enemy class
class Enemy():
	def __init__(self, x, y, size, vel, speed):
		self.rect = pg.Rect(x, y, size, size)
		self.vel = vel
		self.speed = speed
		self.size = size
		self.x = x
		self.y = y

	def move(self):
		self.x += self.vel[0]*self.speed
		self.y += self.vel[1]*self.speed
		self.rect = pg.Rect(round(self.x), round(self.y), self.size, self.size)

	def is_outside(self, w, h):
		if self.x < -2*self.size:
			return True
		elif self.x > w + 2*self.size:
			return True
		elif self.y < -2*self.size:
			return True
		elif self.y > h + 2*self.size:
			return True
		return False

	def draw(self, win):
		pg.draw.rect(win, (255,0,0), self.rect)

# Game class
class Game(Thread):
	def __init__(self, player):
		Thread.__init__(self)
		self.player = player
		self.FRAMERATE = 30
		self.enemy_size = 5
		self.enemy_speed = 3
		self.enemies = []
		self.spawn_timer = 0.25

	def spawn_enemy(self):
		side = random.randint(1, 4)
		frac_pos = random.random()

		# 1-Left, 2-Right, 3-Top, 4-Bottom
		if side == 1:
			x_pos = -self.enemy_size
			y_pos = frac_pos*self.player.h
		if side == 2:
			x_pos = self.player.w
			y_pos = frac_pos*self.player.h
		if side == 3:
			x_pos = frac_pos*self.player.w
			y_pos = -self.enemy_size
		if side == 4:
			x_pos = frac_pos*self.player.w
			y_pos = self.player.h
		vel = self.player.get_direction(x_pos, y_pos)
		self.enemies.append(Enemy(x_pos, y_pos, self.enemy_size, vel, self.enemy_speed))


	def run(self):
		pg.init()

		win = pg.display.set_mode((640, 480))
		while self.player.running:
			t1 = time.time()
			# Handle events
			for event in pg.event.get():
				if event.type == pg.QUIT:
					if not self.player.draw:
						self.player.running = False
				if event.type == pg.KEYDOWN:
					if not self.player.draw and event.key == ord("q"):
						self.player.running = False

			# Calculate stuff
			# Spawn
			if self.spawn_timer <= 0:
				self.spawn_enemy()
				self.spawn_timer = 0.25
			# Move and remove if outside
			for enemy_index in range(len(self.enemies)-1, -1, -1):
				self.enemies[enemy_index].move()
				if self.enemies[enemy_index].is_outside(self.player.w, self.player.h):
					self.enemies.pop(enemy_index)
			
			# Draw stuff
			win.fill((0, 0, 0))
			pg.draw.rect(win, (200, 54, 98), pg.Rect(self.player.x*self.player.w, self.player.y*self.player.h, 10, 10))
			for enemy in self.enemies:
				enemy.draw(win)
			# Update screen
			pg.display.update()
			pg.time.delay(1000//self.FRAMERATE)
			t2 = time.time()
			self.spawn_timer -= t2-t1


# mp setup variables
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

player = Player(True)
player.start()

game = Game(player)
game.start()



