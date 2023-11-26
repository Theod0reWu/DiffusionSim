# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 21:24:11 2023

@author: wut6
"""

from abc import ABC, abstractmethod
import random
import math

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.animation as animation
import numpy as np
from scipy import signal
from scipy.spatial import Delaunay
from scipy.spatial.distance import pdist

from simdata import SimMap, BoundaryCondition, Particle, ParticleMap

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
        plt.clf()

        d = self.simdata.get_data()
        x = [i[0] for i in d]
        y = [i[1] for i in d]
        plt.ylim(0, self.size[1])
        plt.xlim(0, self.size[0])
        plt.scatter(x,y)
        plt.show()

    def __str__(self):
        s = "size: " + str(self.size) + " | particles:" + str(len(self.simdata.get_ids())) +" | boundary: " + str(self.boundary_condition) +"\n"
        s += str(self.simdata.get_data())
        return s

def normalize(vec):
    mag = 0
    for i in vec:
        mag += i ** 2
    return vec / mag ** .5

class ParticleDynamics(Simulation):

    def __init__(self, size : (float, float), boundary_condition : BoundaryCondition):
        super().__init__(size)

        self.simdata = ParticleMap(size)
        self.boundary_condition = boundary_condition

    def add_particle(self, radius : float, position : [float], velocity : [float]):
        self.simdata.add_particle(radius, position, velocity, [0,0])

    def get_data(self):
        pass

    def step(self, dt : float):
        # get projected positions O(n)
        new_positions = {}
        for id in self.simdata.get_ids():
            particle = self.simdata.get_particle(id)
            new_pos = [0 for i in range(particle.dimensions)]
            for p in range(particle.dimensions):
                new_pos[p] = particle.velocity[p] * dt + 1/2 * particle.acc[p] * dt ** 2 + particle.position[p]
            new_positions[id] = new_pos

        #boundary collisions O(n)
        new_velocities = {}
        if (self.boundary_condition == BoundaryCondition.REFLECTIVE):
            for id in self.simdata.get_ids():
                position = new_positions[id]
                if (not self.simdata.in_bounds(position)):
                    if (not id in new_velocities):
                        new_velocities[id] = self.simdata.get_particle(id).velocity
                    for p in range(len(position)):
                        radius = self.simdata.get_particle(id).radius
                        if (position[p] < radius):
                            position[p] = (radius - position[p])
                            new_velocities[id][p] = -1 * new_velocities[id][p]
                        elif(position[p] > self.size[p] - radius):
                            position[p] = 2*self.size[p] - (position[p] + radius)
                            new_velocities[id][p] = -1 * new_velocities[id][p]
                    new_velocities[id]
                new_positions[id] = position

        # particle-particle collisions O(nlogn)
        pos_to_id = {}
        for id in self.simdata.get_ids():
            pos = self.simdata.get_particle(id).position
            pos_to_id[tuple(pos)] = id

        # get all edges in the Delaunay graph
        points_to_check = set()
        points = [i.position for i in self.simdata.get_data()]
        points = np.array(points)
        del_graph = Delaunay(points)
        for triangle in del_graph.simplices:
            ps = np.sort(triangle)
            points_to_check.add((ps[0], ps[1]))
            points_to_check.add((ps[0], ps[2]))
            points_to_check.add((ps[1], ps[2]))
        
        # go from indices to ids
        id_pairs = set()
        for pair in points_to_check:
            id_pairs.add((pos_to_id[tuple(del_graph.points[pair[0]])], pos_to_id[tuple(del_graph.points[pair[1]])])) 

        # check collisions between id pairs
        epsilon = dt / 100
        collided = set()
        for id_pair in id_pairs:
            a = self.simdata.get_particle(id_pair[0])
            b = self.simdata.get_particle(id_pair[1])

            # the particles have collided resolve the collision
            if (pdist([a.position, b.position]) < a.radius + b.radius and (a.moving() or b.moving)):
                normal = np.array(b.position) - np.array(a.position)
                unit_norm = normalize(normal)

                van = np.dot(unit_norm, a.velocity) 
                vbn = np.dot(unit_norm, b.velocity)

                # resolve the positions 
                diff = a.radius + b.radius - pdist([a.position, b.position])
                t_intercept = diff / (np.abs(van) + np.abs(vbn))
                # print("start:", pdist([a.position, b.position]), id_pair, "positions:", a.position, b.position)
                # print("Intercept:", t_intercept, "diff:", diff, "van:", van, "vbn:", vbn)
                # print("velocity:", a.velocity, b.velocity)

                # exact positions when they collided
                a_prev = np.array(a.position) + np.array(a.velocity) * t_intercept * -1
                b_prev = np.array(b.position) + np.array(b.velocity) * t_intercept * -1
                # print(pdist([a_prev, b_prev]), a.radius + b.radius)

                # calculate the velocity after the collision
                normal = np.array(b_prev) - np.array(a_prev)
                unit_norm = normalize(normal)
                tangent = np.array([-1 * unit_norm[1], unit_norm[0]])

                van = np.dot(unit_norm, a.velocity)
                vat = np.dot(tangent, a.velocity)

                vbn = np.dot(unit_norm, b.velocity)
                vbt = np.dot(tangent, b.velocity)

                #elastic collisions equal mass
                new_velocities[id_pair[0]] = vat * tangent + vbn * unit_norm
                new_velocities[id_pair[1]] = vbt * tangent + van * unit_norm
                # print("new_velocities:", new_velocities[id_pair[0]], new_velocities[id_pair[1]])
                
                # t_left = np.array(a.position)
                new_positions[id_pair[0]] = a_prev + new_velocities[id_pair[0]] * (t_intercept + dt)
                new_positions[id_pair[1]] = b_prev + new_velocities[id_pair[1]] * (t_intercept + dt)

        #update all positions and velocities O(n)
        for id in self.simdata.get_ids():
            self.simdata.update_particle_pos(id, new_positions[id])
        for id in new_velocities.keys():
            self.simdata.update_particle_velocity(id, new_velocities[id])

        # https://www.vobarian.com/collisions/2dcollisions2.pdf

    def animate(self, steps : int, dt : float):
        # fig = plt.figure()
        # plt.axis("equal")
        fig, ax = plt.subplots()
        plt.ylim(0, self.size[1])
        plt.xlim(0, self.size[0])

        d = self.simdata.get_data()
        x = [i.position[0] for i in d]
        y = [i.position[1] for i in d]
        r = [i.radius for i in d]
        # im = plt.scatter(x,y)
        for i in range(len(x)):
            c = plt.Circle((x[i],y[i]), r[i])
            ax.add_patch(c)
        def update(i):
            self.step(dt)
            d = self.simdata.get_data()
            x = [i.position[0] for i in d]
            y = [i.position[1] for i in d]
            plt.cla()
            # plt.axis("equal")
            plt.ylim(0, self.size[1])
            plt.xlim(0, self.size[0])
            im = plt.scatter(x,y)
            for i in range(len(x)):
                c = plt.Circle((x[i],y[i]), r[i])
                ax.add_patch(c)

        anim = animation.FuncAnimation(fig, update, interval=2, frames=steps)
        # anim.save("test.gif")
        plt.show()

    def display(self):
        fig, ax = plt.subplots()

        d = self.simdata.get_data()
        x = [i.position[0] for i in d]
        y = [i.position[1] for i in d]
        r = [i.radius for i in d]
        plt.ylim(0, self.size[1])
        plt.xlim(0, self.size[0])

        for i in range(len(x)):
            c = plt.Circle((x[i],y[i]), r[i])
            ax.add_patch(c)
        # plt.scatter(x,y)
        plt.show()

    def simulate(self, steps : int, dt : float):
        for t in range(steps):
            self.step(dt)

