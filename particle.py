# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 21:37:08 2019

@author: sinkovitsd
"""

from vector2 import vector2

class Particle:
    def __init__(self, mass, pos, vel=vector2(0,0), gravity=vector2(0,0)):
        if mass == 0:
            self.invmass = 0
        else:
            self.invmass = 1.0/mass
        self.pos = vector2(pos)
        self.vel = vector2(vel)
        self.gforce = mass*vector2(gravity)
        self.force = vector2(self.gforce)
        self.interactions = []
        self.contacts = []
        
    def integrate(self, dt):
        self.vel += self.invmass*self.force*dt
        self.pos += self.vel*dt
        self.force = vector2(self.gforce)

    def delete(self):
        for i in self.interactions:
            i.remove(self)
        for c in self.contacts:
            c.remove(self)