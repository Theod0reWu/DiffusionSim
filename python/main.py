# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:40:35 2023

@author: wut6
"""

from simulation import CoarseDiffsion
from simdata import BoundaryCondition
import numpy as np

if __name__ == '__main__':
    #define sim parameters
    sim_size = (20,1)
    diffusion_flux = ((.05, .2, .05),(.2, -1, .2),(.05, .2, .05))
    diffusion_rate = .5
    bc = BoundaryCondition.REFLECTIVE
    
    sim =  CoarseDiffsion(sim_size, diffusion_flux, diffusion_rate, bc)
    sim.set_concentration(10,0,10)
    # sim.set_concentration(4,4,1)
    # print(sim)
    sim.display()
    
    sim.step(50, 1, True)
    print(sim)
    sim.display()