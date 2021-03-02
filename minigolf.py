# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 14:28:21 2019

@author: nortonn
"""

import pygame
from circle import Circle
from wall import Wall
from polygon import Polygon
from vector2 import vector2
from hole import Hole
import force
import contact


def main():
    pygame.init()
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 800
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    pygame.display.set_caption("Mini Golf")
    gravity = vector2(0,0) # Downward uniform gravity, set to zero
    
#    drag = 1.5
    power = 3
    stroke = 0
    inSandPit = False
    inSandPit2 = False 
    inGrassPit = False
    inGrassPitRight = False
    inGrassPitLeft = False
    inHill = False
    youWin = False;

    grassCoeff = 2
    sandCoeff = 5
    
    
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    GREEN = (0, 128, 0)
    
    LIGHT_GREY = (128,128,128)
    DARK_GREEN = (11, 102, 35)
    LIGHT_BROWN = (225, 196, 161)
    
    
    # list of objects in world
    objects = []
    #Handles Collisions
    collisions = []
    #Holds the ball and hold
    hole_ball = []

    # list of forces active    
    forces = []
    
    # list of contact generators
    contact_generators = []
    # list of contacts to be resolved
    contacts = []

#    Hole = (Circle(0, vector2(100,100), vector2(0,0), 6, BLACK, gravity))
    DetectionCircle = Circle(0, vector2(150,100), vector2(0,0), 8)
    
    objects.append(Polygon(vector2(350,100), ((300,0), (400,0), (400, 200), (300,200)), LIGHT_GREY))
    collisions.append(Polygon(vector2(350,100), ((300,0), (400,0), (400, 200), (300,200)), LIGHT_GREY))
    
    objects.append(Polygon(vector2(300,350), ((200,200), (400,200), (400, 500), (200,500)), LIGHT_GREY))
    collisions.append(Polygon(vector2(300,350), ((200,200), (400,200), (400, 500), (200,500)), LIGHT_GREY))
    
    objects.append(Polygon(vector2(50,400), ((0,200), (100,200), (100, 600), (0,600)), LIGHT_GREY))
    collisions.append(Polygon(vector2(50,400), ((0,200), (100,200), (100, 600), (0,600)), LIGHT_GREY))

    objects.append(Polygon(vector2(150,700), ((0,600), (300,600), (300, 800), (0,800)), LIGHT_GREY))
    collisions.append(Polygon(vector2(150,700), ((0,600), (300,600), (300, 800), (0,800)), LIGHT_GREY))

    #Triangle1
    objects.append(Polygon(vector2(525,375), ((300,500), (400,500), (400, 600)), LIGHT_GREY))
    collisions.append(Polygon(vector2(525,375), ((300,500), (400,500), (400, 600)), LIGHT_GREY))
#    Triangle2
    objects.append(Polygon(vector2(125,575), ((100, 600), (100, 500), (200,600)), LIGHT_GREY))
    collisions.append(Polygon(vector2(125,575), ((100, 600), (100, 500), (200,600)), LIGHT_GREY))

    
    ball = Circle(1, vector2(350,775), vector2(0,0), 5, WHITE, gravity)
    objects.append(ball)
    objects.append(Hole(0, vector2(150,100), vector2(0,0), 0))
    
    hole_ball.append(ball)
    hole_ball.append(Hole(0, vector2(150,100), vector2(0,0), 0))
    
    collisions.append(ball)
    
    #Top Wall
    objects.append(Wall(vector2(0, 0), vector2(0,1),LIGHT_GREY))
    collisions.append(Wall(vector2(0, 0), vector2(0,1),LIGHT_GREY))

    #left Wall
    objects.append(Wall(vector2(0, 0), vector2(1,0),LIGHT_GREY))
    collisions.append(Wall(vector2(0, 0), vector2(1,0),LIGHT_GREY))

    #Right Wall
    objects.append(Wall(vector2(SCREEN_WIDTH, 0), vector2(-1,0),LIGHT_GREY))
    collisions.append(Wall(vector2(SCREEN_WIDTH, 0), vector2(-1,0),LIGHT_GREY))

    #Bottom Wall
    objects.append(Wall(vector2(0, SCREEN_HEIGHT), vector2(0,-1),LIGHT_GREY))
    collisions.append(Wall(vector2(0, SCREEN_HEIGHT), vector2(0,-1),LIGHT_GREY))


    #Hill Normals
    hill_force = vector2(0,150)
    hill_force2 = vector2(0,-150)

    
    #Start adding forces
    sandForce = force.SingleForce(objects, lambda o1: force.linear_drag(o1, sandCoeff))
    sandForce2 = force.SingleForce(objects, lambda o1: force.linear_drag(o1, sandCoeff))

    grassForce = force.SingleForce(objects, lambda o1: force.linear_drag(o1, grassCoeff))
    grassForceLeft = force.SingleForce(objects, lambda o1: force.linear_drag(o1, grassCoeff))
    grassForceRight = force.SingleForce(objects, lambda o1: force.linear_drag(o1, grassCoeff))
    holeForce = force.PairForce(hole_ball, lambda o1, o2: force.spring_force(o1,o2,100,0))
    hillForce = force.SingleForce(objects, lambda o1: force.hill_drag(hill_force))
    hillForce2 = force.SingleForce(objects, lambda o1: force.hill_drag(hill_force2))


    
    forces.append(force.SingleForce(objects, lambda o1: force.constant_drag(o1)))

    contact_generators.append(contact.ContactGenerator(collisions, 0.5))

    sandPit = (300, 650, 100, 20)
    sandPit2 = (100, 340, 100, 20)
    grassPit = (0, 0, 300, 50)
    grassPitRight = (250, 50, 50, 200)
    grassPitLeft = (0, 50, 50, 200)
    hillArea = (100, 200, 100, 100)
    hillArea2 = (100, 400, 100, 100)

    
    # Main Loop
    done = False
    frame_rate = 60
    dt = 1.0/frame_rate

    clock = pygame.time.Clock()
    while not done:
        # --- Main event loop
        for event in pygame.event.get(): # User did something
            if (event.type == pygame.QUIT # If user clicked close
                or (event.type == pygame.KEYDOWN 
                    and event.key == pygame.K_ESCAPE)): # or pressed ESC
                done = True # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN: # If user clicked 
                if event.button == 1:
                    # Move the player
                    if ball.vel.mag() <= 1 and youWin != True:
                        stroke = stroke + 1
                        x =  pygame.mouse.get_pos()[0] - ball.pos.x
                        y =  pygame.mouse.get_pos()[1] - ball.pos.y 
                        direc = vector2(x,y)
                        ball.vel = direc * power
                # Reset the game
                elif event.button == 3:
                    ball.pos.x = 350
                    ball.pos.y = 775
                    stroke = 0
                    ball.vel = vector2(0,0)
                    youWin = False

        distanceToHole = ball.pos - DetectionCircle.pos
        #Hole force creater
        if distanceToHole.mag() < DetectionCircle.radius:
            if (forces[-1] != holeForce):
                forces.append(holeForce)
        else:
            if (forces[-1] == holeForce):
                forces.remove(holeForce)
        # In sand pit
        if ((ball.pos[0] >= sandPit[0]) and (ball.pos[0] <= sandPit[0] + sandPit[2])):
            if ((ball.pos[1] >= sandPit[1]) and (ball.pos[1] <= sandPit[1] + sandPit[3])):
                inSandPit = True
            else:
                inSandPit = False
        else:
            inSandPit = False
            
        if (inSandPit is True):
            if (forces[-1] != sandForce2):
                forces.append(sandForce2)
        else:
            if (forces[-1] == sandForce2):
                forces.remove(sandForce2)
        #In sand pit 2
        if ((ball.pos[0] >= sandPit2[0]) and (ball.pos[0] <= sandPit2[0] + sandPit2[2])):
            if ((ball.pos[1] >= sandPit2[1]) and (ball.pos[1] <= sandPit2[1] + sandPit2[3])):
                inSandPit2 = True
            else:
                inSandPit2 = False
        else:
            inSandPit2 = False
            
        if (inSandPit2 is True):
            if (forces[-1] != sandForce):
                forces.append(sandForce)
        else:
            if (forces[-1] == sandForce):
                forces.remove(sandForce)
        #Grass Pit
        if ((ball.pos[0] >= grassPit[0]) and (ball.pos[0] <= grassPit[0] + grassPit[2])):
            if ((ball.pos[1] >= grassPit[1]) and (ball.pos[1] <= grassPit[1] + grassPit[3])):
                inGrassPit = True
            else:
                inGrassPit = False
        else:
            inGrassPit = False
            
        if (inGrassPit is True):
            if (forces[-1] != grassForce):
                forces.append(grassForce)
        else:
            if (forces[-1] == grassForce):
                forces.remove(grassForce)
        #Grass Pit Right
        if ((ball.pos[0] >= grassPitRight[0]) and (ball.pos[0] <= grassPitRight[0] + grassPitRight[2])):
            if ((ball.pos[1] >= grassPitRight[1]) and (ball.pos[1] <= grassPitRight[1] + grassPitRight[3])):
                inGrassPitRight = True
            else:
                inGrassPitRight = False
        else:
            inGrassPitRight = False
            
        if (inGrassPitRight is True):
            if (forces[-1] != grassForceRight):
                forces.append(grassForceRight)
        else:
            if (forces[-1] == grassForceRight):
                forces.remove(grassForceRight)
        #Grass Pit Left
        if ((ball.pos[0] >= grassPitLeft[0]) and (ball.pos[0] <= grassPitLeft[0] + grassPitLeft[2])):
            if ((ball.pos[1] >= grassPitLeft[1]) and (ball.pos[1] <= grassPitLeft[1] + grassPitLeft[3])):
                inGrassPitLeft = True
            else:
                inGrassPitLeft = False
        else:
            inGrassPitLeft = False
            
        if (inGrassPitLeft is True):
            if (forces[-1] != grassForceLeft):
                forces.append(grassForceLeft)
        else:
            if (forces[-1] == grassForceLeft):
                forces.remove(grassForceLeft)
        # Hill
        if ((ball.pos[0] >= hillArea[0]) and (ball.pos[0] <= hillArea[0] + hillArea[2])):
            if ((ball.pos[1] >= hillArea[1]) and (ball.pos[1] <= hillArea[1] + hillArea[3])):
                inHill = True
            else:
                inHill = False
        else:
            inHill = False
            
        if (inHill is True):
            if (forces[-1] != hillForce):
                forces.append(hillForce)
        else:
            if (forces[-1] == hillForce):
                forces.remove(hillForce)
        
        # Hill2
        if ((ball.pos[0] >= hillArea2[0]) and (ball.pos[0] <= hillArea2[0] + hillArea2[2])):
            if ((ball.pos[1] >= hillArea2[1]) and (ball.pos[1] <= hillArea2[1] + hillArea2[3])):
                inHill = True
            else:
                inHill = False
        else:
            inHill = False
            
        if (inHill is True):
            if (forces[-1] != hillForce2):
                forces.append(hillForce2)
        else:
            if (forces[-1] == hillForce2):
                forces.remove(hillForce2)

        # Add forces
        for f in forces:
            f.force_all()
        
        # Move objects
        for o in objects:
            o.integrate(dt)
            
        # Get contacts
        niterations = 0
        max_iterations = 10
        while niterations < max_iterations:
            niterations += 1
            contacts = []
            for g in contact_generators:
                contacts.extend(g.contact_all())
              
            if len(contacts)==0:
                break
                
            # Resolve contacts
            contacts.sort(key=lambda x: x.penetration)
            for c in contacts:
                c.resolve()

        # Draw objects to screen
        screen.fill(GREEN) # clears the screen

        pygame.draw.rect(screen, DARK_GREEN, grassPit, 0)
        pygame.draw.rect(screen, DARK_GREEN, grassPitRight, 0)
        pygame.draw.rect(screen, DARK_GREEN, grassPitLeft, 0)
        pygame.draw.rect(screen, (0,255,0), hillArea, 0)
        pygame.draw.rect(screen, (0,200,0), (100, 300, 100, 100 ), 0)
        pygame.draw.rect(screen, (0,255,0), hillArea2, 0)
        pygame.draw.rect(screen, LIGHT_BROWN, sandPit, 0)
        pygame.draw.rect(screen, LIGHT_BROWN, sandPit2, 0)
        pygame.draw.circle(screen, BLACK, vector2(150,100), 6) #Hole

        for o in objects:
            o.draw(screen)
        
        if ball.vel.mag() <= 1 and ball.pos.x > 145 and ball.pos.x < 155 and ball.pos.y > 95 and ball.pos.y < 105:
            if youWin == False:
                print("You win!!!")
                youWin = True;
        elif ball.vel.mag() <= 1:
            pygame.draw.aaline(screen, BLACK, (int(ball.pos.x), int(ball.pos.y)), 
                               (int(pygame.mouse.get_pos()[0]), int(pygame.mouse.get_pos()[1])))        
        #Screen Text
        myfont = pygame.font.SysFont('arial', 30)
        
        stroke_text = myfont.render("Stroke: " + str(stroke), False, BLACK)
        text_rect = stroke_text.get_rect(center=(60, 20))
        
        screen.blit(stroke_text, text_rect)

        
        # Update the screen
        pygame.display.update()

        # --- Limit to 60 frames per second
        clock.tick(60)
        
    pygame.quit()
 
""" Safe start """
if __name__ == "__main__":
    try:
        main()
    except:
        pygame.quit()
        raise