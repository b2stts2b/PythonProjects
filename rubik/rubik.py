#!/usr/bin/env python3
import pygame, sys, scramble
import pygame.gfxdraw

class Cube:
    def __init__(self):
        # indices for turning cube  
        self.moves = {
            "R":[[(0,8), (3,0), (2,8), (1,8)],
                 [(0,5), (3,3), (2,5), (1,5)],
                 [(0,2), (3,6), (2,2), (1,2)],
                 [(5,0), (5,2), (5,8), (5,6)],
                 [(5,1), (5,5), (5,7), (5,3)]],
            "R'":[[(0,8), (1,8), (2,8), (3,0)],
                  [(0,5), (1,5), (2,5), (3,3)],
                  [(0,2), (1,2), (2,2), (3,6)],
                  [(5,0), (5,6), (5,8), (5,2)],
                  [(5,1), (5,3), (5,7), (5,5)]],
            "L":[[(0,6), (1,6), (2,6), (3,2)],
                 [(0,3), (1,3), (2,3), (3,5)],
                 [(0,0), (1,0), (2,0), (3,8)],
                 [(4,0), (4,2), (4,8), (4,6)],
                 [(4,1), (4,5), (4,7), (4,3)]],
            "L'":[[(0,6), (3,2), (2,6), (1,6)],
                  [(0,3), (3,5), (2,3), (1,3)],
                  [(0,0), (3,8), (2,0), (1,0)],
                  [(4,0), (4,6), (4,8), (4,2)],
                  [(4,1), (4,3), (4,7), (4,5)]],
            "U":[[(1,0), (4,0), (3,0), (5,0)],
                 [(1,1), (4,1), (3,1), (5,1)],
                 [(1,2), (4,2), (3,2), (5,2)],
                 [(0,0), (0,2), (0,8), (0,6)],
                 [(0,1), (0,5), (0,7), (0,3)]],
            "U'":[[(1,0), (5,0), (3,0), (4,0)],
                  [(1,1), (5,1), (3,1), (4,1)],
                  [(1,2), (5,2), (3,2), (4,2)],
                  [(0,0), (0,6), (0,8), (0,2)],
                  [(0,1), (0,3), (0,7), (0,5)]],
            "F":[[(0,6), (5,0), (2,2), (4,8)],
                 [(0,7), (5,3), (2,1), (4,5)],
                 [(0,8), (5,6), (2,0), (4,2)],
                 [(1,0), (1,2), (1,8), (1,6)],
                 [(1,1), (1,5), (1,7), (1,3)]],
            "F'":[[(0,6), (4,8), (2,2), (5,0)],
                  [(0,7), (4,5), (2,1), (5,3)],
                  [(0,8), (4,2), (2,0), (5,6)],
                  [(1,0), (1,6), (1,8), (1,2)],
                  [(1,1), (1,3), (1,7), (1,5)]],
            "D":[[(1,6), (5,6), (3,6), (4,6)],
                 [(1,7), (5,7), (3,7), (4,7)],
                 [(1,8), (5,8), (3,8), (4,8)],
                 [(2,0), (2,2), (2,8), (2,6)],
                 [(2,1), (2,5), (2,7), (2,3)]],
            "D'":[[(1,6), (4,6), (3,6), (5,6)],
                  [(1,7), (4,7), (3,7), (5,7)],
                  [(1,8), (4,8), (3,8), (5,8)],
                  [(2,0), (2,6), (2,8), (2,2)],
                  [(2,1), (2,3), (2,7), (2,5)]],
            "B":[[(0,0), (4,6), (2,8), (5,2)],
                 [(0,1), (4,3), (2,7), (5,5)],
                 [(0,2), (4,0), (2,6), (5,8)],
                 [(3,0), (3,2), (3,8), (3,6)],
                 [(3,1), (3,5), (3,7), (3,3)]],
            "B'":[[(0,0), (5,2), (2,8), (4,6)],
                  [(0,1), (5,5), (2,7), (4,3)],
                  [(0,2), (5,8), (2,6), (4,0)],
                  [(3,0), (3,6), (3,8), (3,2)],
                  [(3,1), (3,3), (3,7), (3,5)]]}

        # RGB for all colors
        self.colors = {"Y":(255, 255, 0),
                       "R":(255, 0, 0),
                       "W":(255, 255, 255),
                       "O":(255, 165, 0),
                       "B":(0, 0, 255),
                       "G":(0, 255, 0)}

        # The cube expressed as a 2d-list
        self.sides = [
            ["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"],   #U-layer
            ["R", "R", "R", "R", "R", "R", "R", "R", "R"],   #F-layer
            ["W", "W", "W", "W", "W", "W", "W", "W", "W"],   #D-layer
            ["O", "O", "O", "O", "O", "O", "O", "O", "O"],   #B-layer
            ["B", "B", "B", "B", "B", "B", "B", "B", "B"],   #L-layer
            ["G", "G", "G", "G", "G", "G", "G", "G", "G"]]   #R-layer
        self.side_indices = [0, 1, 5]

        # The polygons for all sides 
        self.polygons =[
            [(300, 90), (270, 100), (300, 110), (330, 100)], #U-layer 1
            [(330, 100), (300, 110), (330, 120), (360, 110)],#U-layer 2
            [(360, 110), (330, 120), (360, 130), (390, 120)],#U-layer 3
            [(270, 100), (300, 110), (270, 120), (240, 110)],#U-layer 4
            [(300, 110), (270, 120), (300, 130), (330, 120)],#U-layer 5
            [(330, 120), (300, 130), (330, 140), (360, 130)],#U-layer 6
            [(240, 110), (210, 120), (240, 130), (270, 120)],#U-layer 7
            [(270, 120), (300, 130), (270, 140), (240, 130)],#U-layer 8
            [(300, 130), (270, 140), (300, 150), (330, 140)],#U-layer 9
            [(240, 130), (240, 170), (210, 160), (210, 120)],#F-layer 1
            [(270, 140), (270, 180), (240, 170), (240, 130)],#F-layer 2
            [(300, 150), (300, 190), (270, 180), (270, 140)],#F-layer 3
            [(240, 170), (240, 210), (210, 200), (210, 160)],#F-layer 4
            [(270, 180), (270, 220), (240, 210), (240, 170)],#F-layer 5
            [(300, 190), (300, 230), (270, 220), (270, 180)],#F-layer 6
            [(240, 210), (240, 250), (210, 240), (210, 200)],#F-layer 7
            [(270, 220), (270, 260), (240, 250), (240, 210)],#F-layer 8
            [(300, 230), (300, 270), (270, 260), (270, 220)],#F-layer 9
            [(300, 150), (300, 190), (330, 180), (330, 140)],#R-layer 1
            [(330, 140), (330, 180), (360, 170), (360, 130)],#R-layer 2
            [(360, 130), (360, 170), (390, 160), (390, 120)],#R-layer 3
            [(300, 190), (300, 230), (330, 220), (330, 180)],#R-layer 4
            [(330, 180), (330, 220), (360, 210), (360, 170)],#R-layer 5
            [(360, 170), (360, 210), (390, 200), (390, 160)],#R-layer 6
            [(300, 230), (300, 270), (330, 260), (330, 220)],#R-layer 7
            [(330, 220), (330, 260), (360, 250), (360, 210)],#R-layer 8
            [(360, 210), (360, 250), (390, 240), (390, 200)] #R-layer 9
            ]

    # Draw cube
    def draw(self, win):
        for i, polygon in enumerate(self.polygons):
            pygame.gfxdraw.filled_polygon(win, polygon, self.colors[self.sides[self.side_indices[i//9]][i%9]])
        for polygon in self.polygons:
            pygame.gfxdraw.polygon(win, polygon, (0,0,0))

    # turn one of the cube's sides
    def turn_cube(self, move):
        for phase in self.moves[move]:
            temp = self.sides[phase[0][0]][phase[0][1]]
            for i in range(-1, -4, -1):
                start = phase[i]
                end = phase[i+1]
                self.sides[end[0]][end[1]] = self.sides[start[0]][start[1]]
            end = phase[1]
            self.sides[end[0]][end[1]] = temp

    # Reset the cube
    def reset_cube(self):
        for side_index, color in enumerate("YRWOBG"):
            for spot_index in range(9):
                self.sides[side_index][spot_index] = color

    # Shuffle cube
    def shuffle_cube(self):
        shuffle = scramble.gen_scramble().split()
        for move in shuffle:
            if "2" in move:
                self.turn_cube(move[0])
                self.turn_cube(move[0])
            else:
                self.turn_cube(move)
            

# Initialize pygame
pygame.init()
has_pressed = False

# Objects
win = pygame.display.set_mode((600, 400))
cube = Cube()

# Main loop
while True:
    # Go through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 27:
                sys.exit()

    # Get input
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_s]:
        if not has_pressed:
            cube.reset_cube()
            has_pressed = True
    elif keys_pressed[pygame.K_SPACE]:
        if not has_pressed:
            cube.shuffle_cube()
            has_pressed = True
    elif keys_pressed[pygame.K_r]:
        if not has_pressed:
            if keys_pressed[pygame.K_LCTRL]:
                cube.turn_cube("R'")
            else:    
                cube.turn_cube("R")
            has_pressed = True
    elif keys_pressed[pygame.K_l]:
        if not has_pressed:
            if keys_pressed[pygame.K_LCTRL]:
                cube.turn_cube("L'")
            else:    
                cube.turn_cube("L")
            has_pressed = True
    elif keys_pressed[pygame.K_u]:
        if not has_pressed:
            if keys_pressed[pygame.K_LCTRL]:
                cube.turn_cube("U'")
            else:    
                cube.turn_cube("U")
            has_pressed = True
    elif keys_pressed[pygame.K_f]:
        if not has_pressed:
            if keys_pressed[pygame.K_LCTRL]:
                cube.turn_cube("F'")
            else:    
                cube.turn_cube("F")
            has_pressed = True
    elif keys_pressed[pygame.K_d]:
        if not has_pressed:
            if keys_pressed[pygame.K_LCTRL]:
                cube.turn_cube("D'")
            else:    
                cube.turn_cube("D")
            has_pressed = True
    elif keys_pressed[pygame.K_b]:
        if not has_pressed:
            if keys_pressed[pygame.K_LCTRL]:
                cube.turn_cube("B'")
            else:    
                cube.turn_cube("B")
            has_pressed = True
    else:
        has_pressed = False

    # Draw
    win.fill((0,0,0))
    cube.draw(win)

    # Update
    pygame.display.update()
    pygame.time.wait(1000//60)