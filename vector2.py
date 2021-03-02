# -*- coding: utf-8 -*-
"""
Created on Fri Jan 25 14:30:50 2019

@author: sinkovitsd
"""

from math import sqrt, sin, cos, floor

class vector2:
    def __init__(self, x, y=None):
        if y==None:
            self.x = x[0]
            self.y = x[1]
        else:
            self.x = x
            self.y = y
        
    # printed representation
    def __repr__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise ValueError("Index out of range.")
            
    def __len__(self):
        return 2
    
    # pygame, friendly output as a tuple of ints    
    def pygame(self):
        return int(floor(self.x + 0.5)), int(floor(self.y + 0.5))
    
    # + operator overload
    def __add__(self, other):
        return vector2(self.x + other.x, self.y + other.y)
    
    # += operator overload
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    
    # - unary operator overload
    def __neg__(self):
        return vector2(-self.x, -self.y)
    
    # - operator overload
    def __sub__(self, other):
        return vector2(self.x - other.x, self.y - other.y)
    
    # -= operator overload
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    
    # * operator overload (dot product and scalar multiplication)
    # when vector (self) is on the left 
    def __mul__(self, other):
        if isinstance(other, vector2):
            return self.x*other.x + self.y*other.y
        else:
            return vector2(self.x*other, self.y*other)
    
    # * operator overload (dot product and scalar multiplication)
    # when vector (self) is on the right 
    def __rmul__(self, other):
        if isinstance(other, vector2):
            return self.x*other.x + self.y*other.y
        else:
            return vector2(self.x*other, self.y*other)
    
    # *= overator overload for scalar multiplication only
    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self
    
    # / operator overload (scalar division only)
    def __truediv__(self, other):
        return vector2(self.x/other, self.y/other)

    # /= operator overload (scalar division only)
    def __idiv__(self, other):
        self.x /= other
        self.y /= other
        return self

    # % operator overload (cross product, treats scalars as vectors in the z axis)
    # when vector (self) is on the left 
    def __mod__(self, other):
        if isinstance(other, vector2):
            return self.x*other.y - self.y*other.x
        else:
            return vector2(self.y*other, -self.x*other)

    # % operator overload (cross product, treats scalars as vectors in the z axis)
    # when vector (self) is on the right
    def __rmod__(self, other):
        if isinstance(other, vector2):
            return -self.x*other.y + self.y*other.x
        else:
            return vector2(-self.y*other, self.x*other)

    # perpendicular to a vector
    def perp(self):
        return vector2(-self.y, self.x) 
    
    # magnitude squared
    def mag2(self):
        return self.x*self.x + self.y*self.y
    
    # magnitude
    def mag(self):
        return sqrt(self.x*self.x + self.y*self.y)
    
    __abs__ = mag # overload abs() operator
    
    # unit vector
    def hat(self):
        mag2 = self.mag2()
        if mag2 == 0:
            return vector2(0,0)
        else:
            return self/sqrt(mag2)

    # rotation to return a new vector
    def rotated(self, radians):
        c = cos(radians)
        s = sin(radians)
        return vector2(self.x*c - self.y*s, self.y*c + self.x*s)
    
    # rotation of this vector in place
    def rotate(self, radians):
        c = cos(radians)
        s = sin(radians)
        tempx = self.x*c - self.y*s
        self.y = self.y*c + self.x*s
        self.x = tempx
  