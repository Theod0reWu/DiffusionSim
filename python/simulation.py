# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:24:11 2023

@author: wut6
"""

from abc import ABC, abstractmethod
import random

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
import numpy as np
from scipy import signal

from simdata import SimMap, BoundaryCondition

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
    def simulate(self, time):
        pass
    
    @abstractmethod
    def get_data(self):
        pass

class CoarseDiffsion(Simulation):
    '''
        Simulates diffusion through the use of dicretized Ficks law
        
        Ficks law: 
            {\displaystyle J=-D{\frac {d\varphi }{dx}}}
            J = -D dphi / dx
        
        D = diffusion coefficient, unit area / unit time
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

    def clear(self):
        self.data = np.array([[0.0 for i in range(size[0])] for e in range(size[1])])
        
    def set_concentration(self, x : int, y : int, concentration : float) -> None:
        self.data[y][x] = concentration
        self.total_concentration = np.sum(self.data)
    
    def step(self, dt : float) -> None:
        scipy_boundary= ""
        if (self.boundary_condition == BoundaryCondition.ABSORBTION):
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
        s = "size: " + str(self.size) + " | diffusion rate: " + str(self.diffusion_rate) + " | boundary: " + str(self.boundary_condition) +"\n"
        s += "Diffusion Flux:\n"
        f = [str(i) for i in self.diffusion_flux]
        s += "\n".join(f) + "\n"
        
        s += "Concentrations:\n"
        d = [str(i) for i in self.data]
        s += "\n".join(d)
        return s

class BrownianMotion(Simulation):
    '''
        Simulated diffusion through Brownian Motion.

        This simulation will use the wierner process to approximate diffusion.
        
        
        
    '''
    def __init__(self, size : (float, float), diffusion_rate : float, boundary_condition : BoundaryCondition):
        super().__init__(size)

        self.simdata = SimMap(size)
        self.diffusion_rate =  diffusion_rate
        self.boundary_condition = boundary_condition

    def copy(self):
        sim = BrownianMotion(self.size, self.diffusion_rate, self.boundary_condition)
        sim.data = self.data.copy()
        return sim

    def add_particle(self, xpos : float, ypos : float):
        self.simdata.add_particle(xpos, ypos)

    def step(self, dt : float):
        keys = self.simdata.get_ids()
        for i in keys:
            point = self.simdata.get_particle(i)
            dx = random.gauss(0, 2 * self.diffusion_rate * dt)
            dy = random.gauss(0, 2 * self.diffusion_rate * dt)
            newx = point[0] + dx
            newy = point[1] + dy

            if (self.boundary_condition == BoundaryCondition.REFLECTIVE):
                if (newx < 0):
                    newx = -1 * newx
                if (newy < 0):
                    newy = -1 * newy

                if (newx > self.size[0]):
                    newx = self.size[0] - newx % self.size[0]
                if (newy > self.size[1]):
                    newy = self.size[1] - newy % self.size[1]

            self.simdata.update_particle(i, newx, newy)

    def simulate(self, steps : int, dt : float, display = False, period = 10):
        time_data = []
        for i in range(steps):
            time_data.append(self.simdata.copy())
            self.step(dt)
            if (display and i % period == 0):
                self.display()
        return time_data
    
    def animate(self, steps : int, dt : float):
        fig = plt.figure()
        plt.axis("equal")
        plt.ylim(0, self.size[1])
        plt.xlim(0, self.size[0])

        d = self.simdata.get_data()
        x = [i[0] for i in d]
        y = [i[1] for i in d]
        im = plt.scatter(x,y)

        def update(i):
            self.step(dt)
            d = self.simdata.get_data()
            x = [i[0] for i in d]
            y = [i[1] for i in d]
            plt.clf()
            plt.axis("equal")
            plt.ylim(0, self.size[1])
            plt.xlim(0, self.size[0])
            im = plt.scatter(x,y)

        anim = animation.FuncAnimation(fig, update, interval=2, frames=steps)
        anim.save("test.gif")
        plt.show()

    def get_data(self):
        pass

    def display(self):
        d = self.simdata.get_data()
        x = [i[0] for i in d]
        y = [i[1] for i in d]

        plt.scatter(x,y)
        plt.show()

    def __str__(self):
        s = "size: " + str(self.size) + " | particles:" + str(len(self.simdata.get_ids())) +" | boundary: " + str(self.boundary_condition) +"\n"
        s += str(self.simdata.get_data())
        return s
