# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:32:02 2023

@author: wut6
"""

from enum import Enum
from abc import ABC, abstractmethod

from scipy.spatial.distance import pdist

class SimData(ABC):
    
    @abstractmethod
    def add_particle(self, id : int):
        pass

    @abstractmethod
    def get_data(self):
        pass

class Particle:

    def __init__(self):
        self.position = [0,0]
        self.velocity = [0,0]
        self.acc = (0,0)

    def __init__(self, radius : float, position : [float], velocity : [float], acc : (float)):
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.acc = acc
        self.dimensions = len(self.position)

    def copy(self):
        return Particle(self.radius, self.position.copy(), self.velocity.copy(), self.acc.copy())

    def step(self, dt):
        for p in range(len(self.position)):
            self.position[p] = self.velocity[p] * dt + 1/2 * self.acc[p] * dt ** 2 + self.position[p]
            self.velocity[p] += self.acc[p] * dt

    def moving(self):
        for i in self.velocity:
            if (i != 0):
                return True
        return False

    def overlap(self, p):
        return pdist([self.position, p.position]) < self.radius + p.radius

    def overlap(self, pos : [float], radius : [float]):
        return pdist([self.position, pos]) < self.radius + radius

    def __str__(self):
        p, v, a = "(", '(', '('
        for d in range(self.dimensions):
            p += str(self.position[d])
            v += str(self.velocity[d])
            a += str(self.acc[d])
            if (d != self.dimensions - 1):
                p += ","
                v += ","
                a += ','
        p += ")"
        v += ")"
        a += ')'
        return "position: " + p + " | velocity: " + v + " | acceleration: " + a


class ParticleMap(SimData):
    def __init__(self, size : (float, float)):
        self.size = size
        self.data = {}
        self.id = 1

    def copy(self):
        copy = ParticleMap(self.size)
        for key in self.data:
            copy.data[key] = self.data[key].copy()
        return copy

    def in_bounds(self, position: [float], radius = 0):
        for p in range(len(self.size)):
            if (position[p] <= radius or position[p] >= self.size[p] - radius):
                return False
        return True
    
    def overlapping(self, radius : float, position : [float]):
        for p in self.get_data():
            if (p.overlap(position, radius)):
                return True
        return False

    def add_particle(self, radius : float, position : [float], velocity : [float], acc : (float, float)):
        # if (self.in_bounds(position) and not self.overlapping(radius, position)):
        if (self.in_bounds(position)):
            self.data[self.id] = Particle(radius, position, velocity, acc)
            self.id += 1
            return self.id - 1
        return False

    def update_particle_pos(self, id : int, position : [float]):
        self.data[id].position = position

    def update_particle_velocity(self, id: int, velocity : [float]):
        self.data[id].velocity = velocity

    def get_particle(self, id: int):
        if (id in self.data):
            return self.data[id]
        return False

    def get_ids(self):
        return self.data.keys()

    def get_data(self):
        return self.data.values()

class SimMap(SimData):

    def __init__(self, size : (float, float)):
        self.size = size
        self.data = {}

        self.id = 1

    def copy(self):
        c = SimMap(self.size)
        c.id = self.id
        c.data = self.data.copy()
        return c

    def clear(self):
        self.data = {}

    def add_particle(self, xpos : float, ypos : float):
        if (xpos > 0 and xpos < self.size[0] and ypos > 0 and ypos < self.size[1]):
            self.data[self.id] = (xpos, ypos)
            self.id += 1
            return self.id - 1
        return False

    def update_particle(self, id : int, xpos:float, ypos : float):
        if (xpos > 0 and xpos < self.size[0] and ypos > 0 and ypos < self.size[1] and id in self.data):
            self.data[id] = (xpos, ypos)
            return True
        return False

    def get_particle(self, id: int):
        if (id in self.data):
            return self.data[id]
        return False

    def get_ids(self):
        return self.data.keys()

    def get_data(self):
        return self.data.values()

class BoundaryCondition(Enum):
    REFLECTIVE = 0
    ABSORBTION = 1