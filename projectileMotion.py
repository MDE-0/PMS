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
screen = pygame.display.set_mode(screenSize)#, pygame.RESIZABLE)
simSize = (math.floor(screenSize[0]*3/4), screenSize[1])
menuSize = (screenSize[0]-simSize[0], screenSize[1])
pygame.display.set_caption("Interactive Projectile Motion Simulation")
screen.fill((0,0,0))

#introduce gui manager
manager = pygame_gui.UIManager(screenSize)
clock = pygame.time.Clock()

#introduce play button
play_button = pygame_gui.elements.UIButton(relative_rect = pygame.Rect((simSize[0], 0), (100, 50)), text = "Play/Stop", manager = manager)


#variables
g = ["g(m/s²)", -98]
psi = ["θ(°)", math.pi/3] #angle of release -> get user input
v = ["u(m/s)", 300] #velocity -> get user input

g_name = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0],50), (120, 50)), text = f"{g[0]}", manager = manager)
g_increase = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+120,50), (50, 50)), text = "↑", manager = manager)
g_decrease = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+170, 50), (50, 50)), text = "↓", manager = manager)
g_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 50), (100, 50)), text = f"{g[1]/10}", manager = manager)

psi_name = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0],100), (120, 50)), text = f"{psi[0]}", manager = manager)
psi_increase = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+120,100), (50, 50)), text = "↑", manager = manager)
psi_decrease = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+170, 100), (50, 50)), text = "↓", manager = manager)
psi_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 100), (100, 50)), text = f"{round(math.degrees(psi[1]))}", manager = manager)

v_name = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0],150), (120, 50)), text = f"{v[0]}", manager = manager)
v_increase = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+120,150), (50, 50)), text = "↑", manager = manager)
v_decrease = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+170, 150), (50, 50)), text = "↓", manager = manager)
v_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 150), (100, 50)), text = f"{v[1]/10}", manager = manager)

vel_arrow_colour = [255,255,255,255]
grav_arrow_colour = [255,255,255,255]

font = pygame.font.SysFont("timesnewroman", 20)


while True:
    time_delta = clock.tick(144)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            exit()
        if event.type == VIDEORESIZE:
            screenSize = (event.w,event.h)
            menuSize = (screenSize[0]-simSize[0],event.h)
            simSize = (math.floor(screenSize[0]*3/4), screenSize[1])
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.update()
    

    #menu loop
    while menu == True:
        time_delta = clock.tick(144)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                exit()
            if event.type == VIDEORESIZE:
                screenSize = (event.w,event.h)
                menuSize = (screenSize[0]-simSize[0],event.h)
                simSize = (math.floor(screenSize[0]*3/4), screenSize[1])
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == play_button:
                        t = 0
                        time_delta = 0
                        t_arrow = 0.3
                        running = True
                        menu = False
                    if event.ui_element == g_decrease:
                        g_value.kill()
                        g[1] -= 2
                        g_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 50), (100, 50)), text = f"{g[1]/10}", manager = manager)
                    if event.ui_element == g_increase:
                        g_value.kill()
                        g[1] += 2
                        g_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 50), (100, 50)), text = f"{g[1]/10}", manager = manager)
                    if event.ui_element == psi_decrease:
                        psi_value.kill()
                        psi[1] -= 5*math.pi/180
                        psi_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 100), (100, 50)), text = f"{round(math.degrees(psi[1]))}", manager = manager)
                    if event.ui_element == psi_increase:
                        psi_value.kill()
                        psi[1] += 5*math.pi/180
                        psi_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 100), (100, 50)), text = f"{round(math.degrees(psi[1]))}", manager = manager)
                    if event.ui_element == v_decrease:
                        v_value.kill()
                        v[1] -= 5
                        v_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 150), (100, 50)), text = f"{v[1]/10}", manager = manager)
                    if event.ui_element == v_increase:
                        v_value.kill()
                        v[1] += 5
                        v_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 150), (100, 50)), text = f"{v[1]/10}", manager = manager)
                
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
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
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
                        
                    if event.ui_element == g_decrease:
                        g_value.kill()
                        g[1] -= 2
                        g_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 50), (100, 50)), text = f"{g[1]/10}", manager = manager)
                    if event.ui_element == g_increase:
                        g_value.kill()
                        g[1] += 2
                        g_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 50), (100, 50)), text = f"{g[1]/10}", manager = manager)
                    if event.ui_element == psi_decrease:
                        psi_value.kill()
                        psi[1] -= 5*math.pi/180
                        psi_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 100), (100, 50)), text = f"{round(math.degrees(psi[1]))}", manager = manager)
                    if event.ui_element == psi_increase:
                        psi_value.kill()
                        psi[1] += 5*math.pi/180
                        psi_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 100), (100, 50)), text = f"{round(math.degrees(psi[1]))}", manager = manager)
                    if event.ui_element == v_decrease:
                        v_value.kill()
                        v[1] -= 5
                        v_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 150), (100, 50)), text = f"{v[1]/10}", manager = manager)
                    if event.ui_element == v_increase:
                        v_value.kill()
                        v[1] += 5
                        v_value = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((simSize[0]+220, 150), (100, 50)), text = f"{v[1]/10}", manager = manager)
                if event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    if event.ui_element == g_name:
                        grav_arrow_colour = [255,255,0,255]
                    if event.ui_element == v_name:
                        vel_arrow_colour = [255,255,0,255]
                elif event.user_type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
                    if event.ui_element == g_name:
                        grav_arrow_colour = [255, 255, 255, 255]
                    if event.ui_element == v_name:
                        vel_arrow_colour = [255, 255, 255, 255]
                    



                        
            manager.process_events(event)
        

        #equations
        # g = -98

        # psi = math.pi/2.5 #angle of release -> get user input
        # v = 300 #velocity -> get user input

        v_x = v[1] * math.cos(psi[1])
        u_y = v[1] * math.sin(psi[1])
        v_y = u_y + g[1]*t

        x_x = -v_x*t
        x_y = ((v_y)**2-(u_y)**2)/(2*g[1])

        x = (x_x, x_y)

        #equations for velocity arrow

        v_x_arrow = v[1] * math.cos(psi[1])
        u_y_arrow = v[1] * math.sin(psi[1])
        v_y_arrow = u_y + g[1]*t_arrow

        x_x_arrow = -v_x_arrow*t_arrow
        x_y_arrow = ((v_y_arrow)**2-(u_y_arrow)**2)/(2*g[1])

        x_arrow = (x_x_arrow, x_y_arrow)

        #collision stuff
        sky = pygame.Rect(0, 0, simSize[0], simSize[1]-100)
        rect1 = pygame.Rect(0,simSize[1]-100,simSize[0],100)
        rect2 = pygame.Rect(- x_x, simSize[1]-100 - x_y, 1, 1)
        collide = rect1.colliderect(rect2)
        if collide:
            t = 0
            t_arrow = 0.3
            menu = True
            running = False
        pygame.draw.rect(simSurface, (100, 100, 100, 100), rect1)
        pygame.draw.rect(simSurface, (100, 100, 100, 100), rect2)
        pygame.draw.rect(simSurface, (0, 0, 255, 0), sky)



        #define arrow
        def draw_arrow(screen, colour, start, end):
            pygame.draw.line(screen,colour,start,end,2)
            rotation = math.degrees(math.atan2(start[1]-end[1], end[0]-start[0]))+90
            pygame.draw.polygon(screen, colour, ((end[0]+5*math.sin(math.radians(rotation)), end[1]+5*math.cos(math.radians(rotation))), (end[0]+5*math.sin(math.radians(rotation-120)), end[1]+5*math.cos(math.radians(rotation-120))), (end[0]+5*math.sin(math.radians(rotation+120)), end[1]+5*math.cos(math.radians(rotation+120)))))
        setattr(pygame.draw, "arrow", draw_arrow)

        
        pygame.draw.arrow(simSurface, grav_arrow_colour, ((- x_x, simSize[1]-100 - x_y)), ((- x_x, simSize[1] - 50 - x_y)))
        pygame.draw.arrow(simSurface, vel_arrow_colour, ((- x_x, simSize[1]-100 - x_y)), ((- x_x_arrow, simSize[1]-100 - x_y_arrow)))


        #Drawing the cannon
        pygame.draw.polygon(simSurface, (255, 255, 255, 255), [(0, simSize[1]-100), (30, simSize[1]-100), (30*math.cos(psi[1]) + 30, (simSize[1]-100 - 30*math.sin(psi[1]))), ((30*math.cos(psi[1])), (simSize[1]-100 - 30*math.sin(psi[1])))])

        
        #HAVE THE USER ADJUST SETTINGS THEN PLAY THE SIMULATION
        #HENCE, INTRODUCE A BUTTON, THAT WHEN PRESSED STARTS DRAWING THE CIRCLE

        grav = g[1]/10
        vel = v[1]/10
        
        halfTime = -vel*math.sin(psi[1])/grav
        totTime = 2*halfTime
        maxHeight = -(vel*math.sin(psi[1]))**2/(2*grav)
        Range = vel*math.cos(psi[1])*totTime

        text1 = font.render(f"The ball's displacement is {round(Range, 2)}m", True, (0, 0, 0))
        text2 = font.render(f"Its maximum height was {round(maxHeight, 2)}m", True, (0, 0, 0))
        text3 = font.render(f"It was above the ground for {round(totTime, 2)}s", True, (0, 0, 0))
        pygame.draw.rect(simSurface, (120, 220, 0), (0,simSize[1]-100,simSize[0],100))
        pygame.draw.circle(simSurface, (255,255,255,255), (- x_x, simSize[1]-100 - x_y), 10)

        #when circle comes into contact with the green floor, KILL THE CIRCLE, DO NOT CLOSE PROGRAM, AND STATE HOW FAR IT TRAVELLED, IT'S MAX HEIGHT AND THE TIME IT WAS ABOVE GROUND
        manager.update(time_delta)
        
        screen.blit(simSurface, (0,0))
        screen.blit(menuSurface, ((math.floor(screenSize[0]*3/4)), 0))
        screen.blit(text1, ((math.floor(screenSize[0]*3/4)), 220))
        screen.blit(text2, ((math.floor(screenSize[0]*3/4)), 260))
        screen.blit(text3, ((math.floor(screenSize[0]*3/4)), 300))
        manager.draw_ui(screen)
        pygame.display.update()
