# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:40:35 2023

@author: wut6
"""

from simulation import CoarseDiffsion, BrownianMotion, ParticleDynamics
from simdata import BoundaryCondition
import numpy as np
import matplotlib.pyplot as plt

import random

def coarse_example_1D():
    #define sim parameters
    sim_size = (21,1)
    diffusion_flux = ((.05, .2, .05),(.2, -1, .2),(.05, .2, .05))
    diffusion_rate = .5
    bc = BoundaryCondition.REFLECTIVE
    
    # create the simulation and show the start
    sim =  CoarseDiffsion(sim_size, diffusion_flux, diffusion_rate, bc)
    sim.set_concentration(10,0,1)
    sim.display()
    
    # run it for 100 timesteps
    timesteps = 201
    data = sim.simulate(timesteps, 1)
    sim.display()

    plt.clf()
    x_int = [i for i in range(21)]
    for i in range(0, len(data), 66):
        t = data[i]

        plt.scatter(x_int,t[0])
        plt.plot(x_int,t[0], label = str(i) + " steps")
    plt.legend(loc="upper left")
    plt.show()

def coarse_animate():
    sim_size = (11,11)
    diffusion_flux = ((.05, .2, .05),(.2, -1, .2),(.05, .2, .05))
    diffusion_rate = .1
    bc = BoundaryCondition.REFLECTIVE
    
    # create the simulation and show the start
    sim =  CoarseDiffsion(sim_size, diffusion_flux, diffusion_rate, bc)
    sim.set_concentration(5,5,1)

    sim.animate(201, 1)

def coarse_example_2D():
    #define sim parameters
    sim_size = (11,11)
    diffusion_flux = ((.05, .2, .05),(.2, -1, .2),(.05, .2, .05))
    diffusion_rate = .1
    bc = BoundaryCondition.REFLECTIVE
    
    # create the simulation and show the start
    sim =  CoarseDiffsion(sim_size, diffusion_flux, diffusion_rate, bc)
    sim.set_concentration(5,5,1)
    sim.display()
    
    # run it for 100 timesteps and show the final state
    timesteps = 400
    data = sim.simulate(timesteps, 1, False, 10)
    sim.display()

def brownian_example():
    sim_size = (11,1)
    diffusion_rate = .1
    bc = BoundaryCondition.REFLECTIVE

    sim = BrownianMotion(sim_size, diffusion_rate, bc)
    for i in range(100):
        sim.add_particle(5, .5)
    # print(sim)

    timesteps = 50
    # data = sim.simulate(timesteps, 1, True, 10)
    sim.animate(timesteps, 1)
    # print(sim)

def collisions_example():
    sim_size = (10,10)
    bc = BoundaryCondition.REFLECTIVE

    sim = ParticleDynamics(sim_size, bc)
    # sim.add_particle(.5, [3, 5], [1, 0])
    # sim.add_particle(.5, [5, 3], [0, 1])
    # sim.add_particle(.5, [7, 5], [-1, 0])
    # sim.add_particle(.5, [4.9, 5], [1, 0])
    # sim.add_particle(.5, [5.1, 5], [0, 1])
    for i in range(500):
        # added = sim.add_particle(.1,[random.uniform(4,6), random.uniform(4,6)], [random.uniform(-1,1), random.uniform(-1,1)])
        # added = sim.add_particle(.1,[random.uniform(4,6), random.uniform(4,6)], [random.gauss(0,1) + .1, .1 + random.gauss(0,1)])
        x = random.uniform(0,10)
        y = random.uniform(0,10)
        d = ((x - 5) ** 2 + (y - 5) ** 2) ** .5

        while not (d <= 4):
            x = random.uniform(0,10)
            y = random.uniform(0,10)
            d = ((x - 5) ** 2 + (y - 5) ** 2) ** .5
        # print(d, x, y)
        
        added = sim.add_particle(.1,[x, y], [random.gauss(0,1) + .1, .1 + random.gauss(0,1)])

        # sim.add_particle(.1,[random.uniform(0,1), random.uniform(0,1)], [0,0])
    sim.display()

    # sim.simulate(12, 1)
    # sim.display()

    sim.animate(100, .05)


if __name__ == '__main__':
    # coarse_example_1D()

    # coarse_animate()

    # coarse_example_2D()

    # brownian_example()

    collisions_example()