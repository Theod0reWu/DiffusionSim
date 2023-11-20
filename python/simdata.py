# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:32:02 2023

@author: wut6
"""

from enum import Enum
from abc import ABC, abstractmethod

class SimData(ABC):
    
    def get_data(self):
        pass
    

class BoundaryCondition(Enum):
    REFLECTIVE = 0
    INFINITE = 1