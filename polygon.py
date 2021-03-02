# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:14:55 2019

@author: Nick
"""
from particle import Particle
from vector2 import vector2
import pygame

class Polygon(Particle):
    def __init__(self, pos, points, color=(0,0,0)):
        super().__init__(0, pos)
        self.normals = []
        self.color = color
        self.points = []
        for p in points:
            self.points.append(vector2(p))
        for i in range(len(points)):
            self.normals.append((self.points[i]-self.points[i-1]).perp().hat())
#            print(self.normals[i])
            
        for i in range(len(self.normals)):
            for p in self.points:
                positive = 0
                negative = 0
                d = (p-self.points[i])*self.normals[i]
                if d > 0:
                    positive += 1
                elif d < 0:
                    negative += 1
                if positive > 0:
                    if negative == 0:
                        self.normals[i]*=-1
                    else:
                        print("This is a Non-convex polygon")
        
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)
        for i in range(len(self.points)):
#            pygame.draw.line(screen,(255,0,0), self. points[i], self.points[i]+self.normals[i]*50,2)
            pass
