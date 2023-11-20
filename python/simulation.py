# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:24:11 2023

@author: wut6
"""

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import matplotlib.colors as colors
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
        
    def set_concentration(self, x : int, y : int, concentration : float) -> None:
        self.data[y][x] = concentration
        self.total_concentration = np.sum(self.data)
    
    def step(self, dt : float) -> None:
        scipy_boundary= ""
        if (self.boundary_condition == BoundaryCondition.INFINITE):
            scipy_boundary = "fill"
        elif (self.boundary_condition == BoundaryCondition.REFLECTIVE):
            scipy_boundary = "symm"
        self.data += (self.diffusion_rate * dt *
                      signal.convolve2d(self.data, self.diffusion_flux, mode='same', boundary=scipy_boundary, fillvalue=0))

    def simulate(self, steps : int, dt : float, display = False, period = 10):
        time_data = []
        for i in range(steps):
            time_data.append(self.data.copy())
            self.step(dt)
            if (display and i % period == 0):
                self.display()
        return time_data

    def get_data(self):
        return self.data

    def display(self):
        color_map = 'hot' # 'Blues' 
        plt.clf()
        disp = self.data
        plt.imshow(disp, cmap=color_map, vmin=0, vmax=self.total_concentration/(self.size[0] * self.size[1] / 2))

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

class BrownianMotion(Simulation):

    def __init__(self, size : (float, float)):
        super().__init__(size)

