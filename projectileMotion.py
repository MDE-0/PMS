import pygame
from pygame.locals import *
import pygame_gui
import math
import numpy
import sys
import time


pygame.init()
running = False
menu = True


screenSize = (1280, 720)
screen = pygame.display.set_mode(screenSize)
simSize = (math.floor(screenSize[0]*3/4), screenSize[1])
menuSize = (screenSize[0]-simSize[0], screenSize[1])
pygame.display.set_caption("Interactive Projectile Motion Simulation")
screen.fill((0,0,0))

#introduce gui manager
manager = pygame_gui.UIManager(screenSize)
clock = pygame.time.Clock()

#introduce play button
play_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((simSize[0], 0), (100, 50)), text = "Play/Stop", manager = manager)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and even.key == K_ESCAPE):
            pygame.quit()
            exit()
    

    #menu loop
    while menu == True:
        time_delta = clock.tick(144)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and even.key == K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        t = 0
                        time_delta = 0
                        t_arrow = 0.3
                        running = True
                        menu = False
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    #main loop
    while running == True:
        time_delta = clock.tick(144)/1000.0
        t += 1/100
        t_arrow += 1/100
        time.sleep(0.001)
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

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        t = 0
                        t_arrow = 0.3
                        menu = True
                        running = False
                        
            manager.process_events(event)
        

        #equations
        g = -98

        psi = math.pi/2.5 #angle of release -> get user input
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

        #collision stuff
        rect1 = pygame.Rect(0,620,960,100)
        rect2 = pygame.Rect(- x_x, 620 - x_y, 1, 1)
        collide = rect1.colliderect(rect2)
        if collide:
            t = 0
            t_arrow = 0.3
            menu = True
            running = False
        pygame.draw.rect(simSurface, (100, 100, 100, 100), rect1)
        pygame.draw.rect(simSurface, (100, 100, 100, 100), rect2)



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
        
        screen.blit(simSurface, (0,0))
        screen.blit(menuSurface, ((math.floor(screenSize[0]*3/4)), 0))    
        manager.draw_ui(screen)
        pygame.display.update()
