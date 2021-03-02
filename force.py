# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 13:30:15 2019

@author: sinkovitsd
"""

from vector2 import vector2

# For forces that interact with one object, such as drag
class SingleForce:
    def __init__(self, objects, force_function):
        self.objects = objects
        self.force_function = force_function
        for o in self.objects:
            o.interactions.append(self)
    
    def force_all(self):
        # Loop through all objects
        for obj in self.objects:
            obj.force += self.force_function(obj)

    def remove(self, obj):
        obj.interactions.remove(self)
        self.objects.remove(obj)

    def delete(self):
        for o in self.objects:
            o.interactions.remove(self)
        self.objects.clear()

# For pair forces, such as gravitation or spring bonds
class PairForce:
    def __init__(self, objects, force_function):
        self.objects = objects
        self.force_function = force_function
        for o in objects:
            o.interactions.append(self)
    
    def force_all(self):
        # Loop through all pairs once
        for i in range(1, len(self.objects)):
            obj1 = self.objects[i]
            for j in range(i):
                obj2 = self.objects[j]
                force = self.force_function(obj1, obj2)
                obj1.force += force
                obj2.force -= force

    def remove(self, obj):
        self.objects.remove(obj)
        
    def draw(screen):
        pass            

def constant_drag(obj):
    return -obj.vel

def linear_drag(obj, coeff):
    return -obj.vel*coeff
  
def hill_drag(normal):
    return normal

def push_force(obj, amount, direc):
    
    return direc.hat()*amount


def gravity_force(obj1, obj2, G):
    r = obj1.pos - obj2.pos
    rmag = r.mag()
    if rmag > obj1.radius + obj2.radius:
        return -G/(obj1.invmass*obj2.invmass*r.mag2())*r.hat()
    else:
        return vector2(0,0)
      
def spring_force(obj1, obj2, k, l):
    r = obj1.pos - obj2.pos
    rmag = r.mag()
    if rmag > obj1.radius + obj2.radius:
        return -k*(rmag-l)*r.hat()
    else:
        return vector2(0,0)
    
def hole_force(obj1, obj2, G):
    r = obj1.pos - obj2.pos
    rmag = r.mag()
    if rmag > obj1.radius + obj2.radius and rmag != 0 and r != 0:
        return -G/(obj1.invmass*obj2.invmass*r.mag2())*r.hat()
    else:
        return vector2(0,0)
    
