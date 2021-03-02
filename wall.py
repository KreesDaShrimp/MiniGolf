# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 21:00:50 2019

@author: Nick
"""

from particle import Particle
from vector2 import vector2
import pygame

class Wall(Particle):
    def __init__(self, pos, normal, color=(0,0,0), length=1000):
        super().__init__(0, pos, vector2(0,0), vector2(0,0))
        self.normal = normal.hat()
        self.color = color
        self.length = length
        
    def draw(self, screen):
        tangent = self.normal.perp()
        p1 = (self.pos + self.length*tangent).pygame()
        p2 = (self.pos - self.length*tangent).pygame()
        pygame.draw.line(screen, self.color, p1, p2)


