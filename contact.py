# -*- coding: utf-8 -*-
"""
Created on Fri Feb 22 11:14:47 2019

@author: sinkovitsd
"""
from vector2 import vector2
from circle import Circle
from wall import Wall
from polygon import Polygon
from math import sqrt
from hole import Hole

class Contact:
    def __init__(self, obj1, obj2, restitution, normal, penetration):
        self.obj1 = obj1
        self.obj2 = obj2
        self.restitution = restitution
        self.normal = normal
        self.penetration = penetration
        
    def resolve(self):
        self.resolve_velocity()
        self.resolve_penetration()
        
    def resolve_penetration(self):
        if self.penetration > 0:
            total_invmass = self.obj1.invmass + self.obj2.invmass
            nudge = self.penetration/total_invmass
            self.obj1.pos += (self.obj1.invmass*nudge)*self.normal
            self.obj2.pos -= (self.obj2.invmass*nudge)*self.normal

    def resolve_velocity(self):
        sep_vel = (self.obj1.vel - self.obj2.vel)*self.normal
        if sep_vel < 0:
            target_sep_vel = -self.restitution*sep_vel
            delta_vel = target_sep_vel - sep_vel
            total_invmass = self.obj1.invmass + self.obj2.invmass
            if total_invmass > 0:
                impulse = delta_vel/total_invmass
                self.obj1.vel += (self.obj1.invmass*impulse)*self.normal
                self.obj2.vel -= (self.obj2.invmass*impulse)*self.normal

class ContactGenerator:
    def __init__(self, objects, restitution=0):
        self.objects = objects
        self.restitution = restitution
        for o in objects:
            o.contacts.append(self)
        self.contacts = []
    
    def remove(self, obj):
        self.objects.remove(obj)
        
    def contact_all(self):
        self.contacts.clear()
        # Loop through all pairs once
        for i in range(1, len(self.objects)):
            obj1 = self.objects[i]
            for j in range(i):
                obj2 = self.objects[j]
                if isinstance(obj1, Circle) and isinstance(obj2, Circle):
                    self.contact_circle_circle(obj1, obj2)
                elif isinstance(obj1, Circle) and isinstance(obj2, Wall):
                    self.contact_circle_wall(obj1, obj2)
                elif isinstance(obj1, Wall) and isinstance(obj2, Circle):
                    self.contact_circle_wall(obj2, obj1)
                elif isinstance(obj1, Wall) and isinstance(obj2, Wall):
                    pass
                elif isinstance(obj1, Circle) and isinstance(obj2, Hole):
                    pass
                elif isinstance(obj1, Hole) and isinstance(obj2, Circle):
                    pass
                elif isinstance(obj1, Hole) and isinstance(obj2, Wall):
                    pass
                elif isinstance(obj1, Wall) and isinstance(obj2, Hole):
                    pass
                elif isinstance(obj1, Polygon) and isinstance(obj2, Hole):
                    pass
                elif isinstance(obj1, Hole) and isinstance(obj2, Polygon):
                    pass
                elif isinstance(obj1, Polygon) and isinstance(obj2, Wall):
                    pass
                elif isinstance(obj1, Wall) and isinstance(obj2, Polygon):
                    pass
                elif isinstance(obj1, Circle) and isinstance(obj2, Polygon):
                    self.contact_circle_polygon(obj1, obj2)
                elif isinstance(obj1, Polygon) and isinstance(obj2, Circle):
                    self.contact_circle_polygon(obj2, obj1)
                elif isinstance(obj1, Polygon) and isinstance(obj2, Polygon):
                    pass
                else:
                    print("Warning! ContactGenerator not implemented between ",
                          type(obj1)," and ", type(obj2),".")
        return self.contacts

    def contact_circle_circle(self, obj1, obj2):
        r = obj1.pos - obj2.pos
        rmag2 = r.mag2()
        R = obj1.radius + obj2.radius
        if rmag2 < R*R:
            rmag = sqrt(rmag2)
            penetration = R - rmag
            normal = r/rmag
            self.contacts.append(Contact(obj1, obj2, self.restitution, normal, penetration))

    def contact_circle_wall(self, circle, wall):
        penetration = (wall.pos - circle.pos) * wall.normal + circle.radius
        if penetration > 0:
            self.contacts.append(Contact(circle, wall, self.restitution, wall.normal, penetration))
    def contact_circle_polygon(self, Circle, Polygon):
        least_penetration = 1e99
        least_depth = 1e99
        least_restitution = 0
        max_penetration = -1e99
        for i in range(len(Polygon.points)):
            P = (Polygon.points[i]-Circle.pos)*Polygon.normals[i]+Circle.radius
            if P <= least_penetration:
                if P <= 0:
                    return
                least_penetration = P
                least_normal = Polygon.normals[i]
        for r in Polygon.points:
            d2 = (r - Circle.pos).mag2()
            if d2 < least_depth:
                least_depth = d2
                least_restitution = r
        n = (least_restitution - Circle.pos).hat()
        rw = Circle.pos + (Circle.radius*n)
        for r in Polygon.points:
            p = (rw - r)*n + Circle.radius
            if P >= max_penetration:
                max_penetration = p
        if max_penetration<0:
            return
        if max_penetration<least_penetration:
            self.contacts.append(Contact(Polygon, Circle, self.restitution, n, max_penetration))
        else:
            self.contacts.append(Contact(Circle, Polygon, self.restitution, least_normal, least_penetration))
            
