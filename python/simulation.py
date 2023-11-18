# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:24:11 2023

@author: wut6
"""

from abc import ABC, abstractmethod
import matplotlib.pyplot as plt

class Simulation(ABC):
    '''
        Simulation class that defines a basic particle simulation
        
        Methods:
            
    '''
    def __init__(self, size : (float, float)):
        self.size = size
        
    @abstractmethod
    def step():
        pass
    
    @abstractmethod
    def get_data():
        pass

class CoarseDiffsion(Simulation):
    
    def __init__(self, size : (int, int), diffusion_rate: ((float), (float), (float)) ):
        super().__init__(size)
        
        self.data = [[[] for i in range(size[0])] for e in range(size[1])]
        self.diffusion_rate = diffusion_rate
        
    def step():
        pass
    
    def get_data():
        pass