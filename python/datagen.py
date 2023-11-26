from simulation import CoarseDiffsion, BrownianMotion, ParticleDynamics
from simdata import BoundaryCondition
import numpy as np

import sys
import random

def main():
	if (len(sys.argv) != 8):
		print("Improper Number of commandline arguments: $ python datagen.py <wierner/collision> <width> <height> <num particles> <timesteps> <dt> <output path>")
		return None
	sim = None
	sim_size = (int(sys.argv[2]), int(sys.argv[3]))
	if (sys.argv[1].lower() == "wierner"):
		diffusion_rate = .1
		sim = BrownianMotion(sim_size, diffusion_rate, BoundaryCondition.REFLECTIVE)
		for n in range(int(sys.argv[4])):
			sim.add_particle(random.uniform(0,sim_size[0]), random.uniform(0,sim_size[1]))
	elif (sys.argv[1].lower() == "collision"):
		sim = ParticleDynamics(sim_size, BoundaryCondition.REFLECTIVE)
		for n in range(int(sys.argv[4])):
			sim.add_particle(.1, [random.uniform(0,sim_size[0]), random.uniform(0,sim_size[1])], [random.uniform(-1,1), random.uniform(-1,1)])
	else:
		print(sys.argv[1] + " is not a proper argument")

	sim.get_data(sys.argv[7], int(sys.argv[5]), float(sys.argv[6]))


# $ python datagen.py <wierner/collision> <width> <height> <num particles> <timesteps> <dt> <output path>
if __name__ == '__main__':
	main()