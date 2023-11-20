# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:24:11 2023

@author: wut6
"""

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from simdata import SimData, BoundaryCondition

class Simulation(ABC):
    '''
        Simulation class that defines a basic particle simulation
        
        Methods:
            
    '''
    def __init__(self, size : (float, float)):
        self.size = size
        
    @abstractmethod
    def step(self):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

class CoarseDiffsion(Simulation):
    '''
        Simulates diffusion through the use of dicretized Ficks law
        
        Ficks law: 
            {\displaystyle J=-D{\frac {d\varphi }{dx}}}
            J = -D dphi /dx
        
        D = diffusion coefficient, unit area / s^2
        J = diffusion flux. the dimension is the amount of substance per unit area per unit time
            It measures the amount of substance that will flow through a unit area 
            during a unit time interval.
        phi = is the concentration, with a dimension of amount of substance per unit volume.
    '''
    
    def __init__(self, size : (int, int), 
                 diffusion_flux: ((float), (float), (float)), 
                 diffusion_rate : float,
                 boundary_condition : BoundaryCondition
                 ):
        super().__init__(size)
        
        self.data = np.array([[0.0 for i in range(size[0])] for e in range(size[1])])
        self.diffusion_flux = np.array(diffusion_flux)
        self.diffusion_rate = diffusion_rate
        self.boundary_condition = boundary_condition
        self.total_concentration = 0
        
    def set_concentration(self, x : int, y : int, concentration : float):
        self.data[y][x] = concentration
        self.total_concentration = np.sum(self.data)
    
    def step(self, steps : float, dt : float, display = False, period = 10):
        scipy_boundary= ""
        if (self.boundary_condition == BoundaryCondition.INFINITE):
            scipy_boundary = "fill"
        elif (self.boundary_condition == BoundaryCondition.REFLECTIVE):
            scipy_boundary = "symm"
        for i in range(steps):
            self.data += (self.diffusion_rate * dt *
                      signal.convolve2d(self.data, self.diffusion_flux, mode='same', boundary=scipy_boundary, fillvalue=0))
            if (display and i % period == 0):
                self.display()
    def get_data(self):
        pass
    
    def print_display(self):
        pass

    def display(self):
        color_map = 'hot' #'Spectral'
        plt.clf()
        plt.imshow(np.round(self.data, 3),cmap=color_map, vmin=0.0, vmax=self.total_concentration)
        plt.axis('off')
        plt.show()
    
    def __str__(self):
        s = "size: " + str(self.size) + " | diffusion rate: " + str(self.diffusion_rate) + "\n"
        s += "Diffusion Flux:\n"
        f = [str(i) for i in self.diffusion_flux]
        s += "\n".join(f) + "\n"
        
        s += "Concentrations:\n"
        d = [str(i) for i in self.data]
        s += "\n".join(d)
        return s