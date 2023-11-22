# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:40:35 2023

@author: wut6
"""

from simulation import CoarseDiffsion, BrownianMotion
from simdata import BoundaryCondition
import numpy as np
import matplotlib.pyplot as plt

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
    print(sim)

    timesteps = 50
    # data = sim.simulate(timesteps, 1, True, 10)
    sim.animate(timesteps, 1)
    print(sim)


if __name__ == '__main__':
    # coarse_example_1D()

    # coarse_example_2D()

    brownian_example()