#!/usr/bin/env python3
from hashlib import new
from pickle import TRUE
import pygame, sys, os, time
from random import randint

class Spawner:
    def __init__(self, win, surf, win_width, win_height):
        self.surf = surf
        self.win = win
        self.h = surf.get_height()
        self.w = surf.get_width()
        self.y = -self.h
        self.x = 0
        self.enemies = []
        self.enemy_speed = 15
        self.spawn_timer = 1
        self.spawn_time = 0.25
        self.time = 0
        self.hasSpawn = False
        self.win_width = win_width
        self.win_height = win_height

    def spawn_enemy(self):
        if self.spawn_timer <= 0:
            x_coord = randint(0, self.win_width-self.w)
            self.enemies.append(Enemy(self.surf, x_coord, self.y, self.w, self.h, self.enemy_speed))
            self.spawn_timer += self.spawn_time

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw(self.win)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.move()

    def check_boundary(self):
        for i in range(len(self.enemies)-1 , -1, -1):
            if self.enemies[i]:
                pass
    
    def remove_dead_enemies(self):
        for i in range(len(self.enemies)-1, -1, -1):
            if self.enemies[i].rect.top > self.win_height:
                del self.enemies[i]

    def start_time(self):
        self.time = time.time()
    
    def end_time(self):
        total_time = time.time()-self.time
        self.spawn_timer -= total_time

class Enemy:
    def __init__(self, surf, x, y, w, h, speed):
        self.surf = surf.copy()
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

    def move(self):
        self.rect = self.rect.move(0, self.speed)

    def draw(self, win):
        win.blit(self.surf, self.rect)

class Runner:
    def __init__(self, win_width, win_height):
        self.rect = pygame.Rect(0, 0, 64, 64) 
        self.win_width = win_width
        self.rect.midbottom = [win_width//2, win_height]
        self.srf_run_stances_right = []
        self.srf_run_stances_left = []
        self.run_index = 0
        self.speed = 10
        self.run_dir = 1
        self.lives = 10
        self.time = 0
        self.setup()

    def setup(self):
        for i in range(1, 8):
            self.srf_run_stances_right.append(pygame.image.load(os.path.join("frames", f"run{i}.png")))
        for stance in self.srf_run_stances_right:
            newStance = stance.copy()
            self.srf_run_stances_left.append(pygame.transform.flip(newStance, True, False))
        self.srf_run = [0, self.srf_run_stances_right, self.srf_run_stances_left]

    def limit_pos(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.win_width:
            self.rect.right = win_width

    def check_collision(self, object):
        if self.rect.colliderect(object.rect):
            self.lives -= 1
            return True
        return False
    
    def start_time(self):
        self.time = time.time()

    def end_time(self):
        print(f"TID: {round(time.time()-self.time,2)}")

# Set up and globals
pygame.init()
win_width, win_height = 400, 600
win = pygame.display.set_mode((win_width, win_height))
FRAMERATE = 30


# Load images
srf_bomb = pygame.image.load(os.path.join("frames", "bomb.png"))

# Objects
spawner = Spawner(win, srf_bomb, win_width, win_height)
runner = Runner(spawner.win_width, spawner.win_height)

runner.start_time()
while True:
    spawner.start_time()
    # Go through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                sys.exit()
    
    # Check key presses
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_RIGHT]:
        runner.run_dir = 1
    elif keys_pressed[pygame.K_LEFT]:
        runner.run_dir = -1
    
    spawner.spawn_enemy()

    # Move/Change stuff
    runner.rect = runner.rect.move(runner.speed*runner.run_dir, 0)
    runner.limit_pos()
    runner.run_index = (runner.run_index + 1)%(len(runner.srf_run[1])*FRAMERATE//15)
    spawner.move_enemies()

    # Remove dead enemies
    spawner.remove_dead_enemies()

    # Check collision
    for i in range(len(spawner.enemies)-1,-1,-1):
        did_hit = runner.check_collision(spawner.enemies[i])
        if did_hit:
            del spawner.enemies[i]

    # Draw stuff
    win.fill((38, 44, 112))
    win.blit(runner.srf_run[runner.run_dir][runner.run_index//(FRAMERATE//15)], runner.rect)
    spawner.draw_enemies()    


    # Update frame
    pygame.display.update()
    if runner.lives <= 0:
        runner.end_time()
        sys.exit()
    pygame.time.wait(1000//FRAMERATE)
    spawner.end_time()