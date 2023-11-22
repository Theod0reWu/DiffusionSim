# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:32:02 2023

@author: wut6
"""

from enum import Enum
from abc import ABC, abstractmethod

class SimData(ABC):
    
    @abstractmethod
    def add_particle(self, id : int):
        pass

    @abstractmethod
    def update_particle(self, id : int):
        pass

    @abstractmethod
    def get_data(self):
        pass

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