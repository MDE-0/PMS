import pygame
from pygame.locals import *
import pygame_gui
import math
import numpy
import sys


pygame.init()
running = True


screenSize = (1280, 720)
screen = pygame.display.set_mode(screenSize)
simSize = (math.floor(screenSize[0]*3/4), screenSize[1])
menuSize = (screenSize[0]-simSize[0], screenSize[1])
pygame.display.set_caption("Interactive Projectile Motion Simulation")
screen.fill((0,0,0))

#introduce gui manager
manager = pygame_gui.UIManager(menuSize)
clock = pygame.time.Clock()

#introduce play button
play_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((0,0), (100, 50)), text = "Play/Stop", manager = manager)

#main loop
while running == True:
    time_delta = clock.tick(144)/1000.0
    t = pygame.time.get_ticks()/1000
    t_arrow = (pygame.time.get_ticks()+300)/1000
    simSurface = pygame.Surface(simSize)
    simSurface.fill((0, 0, 0))
    menuSurface = pygame.Surface(menuSize)
    menuSurface.fill((200,200,200))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and even.key == K_ESCAPE):
            pygame.quit()
            exit()

    #resizing the window: [DO WE WANT IT SCALABLE? it might mess with our program...]
        if event.type == VIDEORESIZE:
            screenSize = (event.w,event.h)
            menuSize = (menuSize[0],event.h)
            simSize = (screenSize[0] - menuSize[0], screenSize[1])
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        
        manager.process_events(event)
    

    #equations
    g = -98

    psi = math.pi/3 #angle of release -> get user input
    v = 300 #velocity -> get user input

    v_x = v * math.cos(psi)
    u_y = v * math.sin(psi)
    v_y = u_y + g*t

    x_x = -v_x*t
    x_y = ((v_y)**2-(u_y)**2)/(2*g)

    x = (x_x, x_y)

    #equations for velocity arrow

    v_x_arrow = v * math.cos(psi)
    u_y_arrow = v * math.sin(psi)
    v_y_arrow = u_y + g*t_arrow

    x_x_arrow = -v_x_arrow*t_arrow
    x_y_arrow = ((v_y_arrow)**2-(u_y_arrow)**2)/(2*g)

    x_arrow = (x_x_arrow, x_y_arrow)


    #define arrow
    def draw_arrow(screen, colour, start, end):
        pygame.draw.line(screen,colour,start,end,2)
        rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
        pygame.draw.polygon(screen, colour, ((end[0]+5*math.sin(math.radians(rotation)), end[1]+5*math.cos(math.radians(rotation))), (end[0]+5*math.sin(math.radians(rotation-120)), end[1]+5*math.cos(math.radians(rotation-120))), (end[0]+5*math.sin(math.radians(rotation+120)), end[1]+5*math.cos(math.radians(rotation+120)))))
    setattr(pygame.draw, "arrow", draw_arrow)
    pygame.draw.arrow(simSurface, [255, 255, 255, 255], ((- x_x, 620 - x_y)), ((- x_x, 660 - x_y)))
    pygame.draw.arrow(simSurface, [255, 255, 255, 255], ((- x_x, 620 - x_y)), ((- x_x_arrow, 620 - x_y_arrow)))


    #Drawing the cannon
    pygame.draw.polygon(simSurface, (255, 255, 255, 255), [(0, 620), (30, 620), (30*math.cos(psi) + 30, (620 - 30*math.sin(psi))), ((30*math.cos(psi)), (620 - 30*math.sin(psi)))])

    
    #HAVE THE USER ADJUST SETTINGS THEN PLAY THE SIMULATION
    #HENCE, INTRODUCE A BUTTON, THAT WHEN PRESSED STARTS DRAWING THE CIRCLE
    pygame.draw.rect(simSurface, (120, 220, 0), (0,620,960,100))
    pygame.draw.circle(simSurface, (255,255,255,255), (- x_x, 620 - x_y), 10)

    #when circle comes into contact with the green floor, KILL THE CIRCLE, DO NOT CLOSE PROGRAM, AND STATE HOW FAR IT TRAVELLED, IT'S MAX HEIGHT AND THE TIME IT WAS ABOVE GROUND
    manager.update(time_delta)
    manager.draw_ui(menuSurface)
    screen.blit(simSurface, (0,0))
    screen.blit(menuSurface, ((math.floor(screenSize[0]*3/4)), 0))    
    pygame.display.update()
