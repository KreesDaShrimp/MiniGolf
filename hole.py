# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:41:34 2019

@author: not sinkovitsd
"""

from particle import Particle
from vector2 import vector2
import pygame

class Hole(Particle):
    def __init__(self, mass, pos, vel, radius, color=(0,0,0), gravity=vector2(0,0)):
        super().__init__(mass, pos, vel, gravity)
        self.radius = radius
        self.color = color
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.pygame(), int(self.radius+0.5))
