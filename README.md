# DiffusionSim
Diffusion Simulation using particle dynamics
<br>
Includes discretized simulations following ficks law, brownian motion modeled by random walks (wierner process) and step-based simulations of elastic collisions.
The graph below shows the concentrations of a disretized simulation in a 1-D line. The concentrations should become uniform over time.
![image](https://github.com/Theod0reWu/DiffusionSim/assets/43049406/2a34b0ae-43e8-4103-a8e4-e7db204f2bc2)
<br>
The gif below shows the same simulation but with the wierner process:
![test](https://github.com/Theod0reWu/DiffusionSim/assets/43049406/f3086a7a-be3d-497c-ba16-ecbeb87c4588)
<br>
The gif below show the simulation done for elastic particle collisions
![test_particle](https://github.com/Theod0reWu/DiffusionSim/assets/43049406/c618f45a-6bdf-4bc7-88b9-2321ade82861)
<br>
# Data Generation
Generate data using the datagen.py file: <br>
```
python datagen.py <wierner/collision> <width> <height> <num particles> <timesteps> <dt> <output path>
```
<br>
- weiner will use the wierner process to generate data (faster), collision will use elastic collusions (slower)
<br>
- width and height are the dimensions of the simulation
<br>
- num particles will place that many particles uniformly into the simulation space (for the collision simulation the velocity is chosen randomly from [0,1]).
<br>
- timesteps is how many timesteps to simulate
<br>
- dt is the amount of time that will elapse for each timestep

# Simulation Results Query

## Running the analysis tool

The analysis tool allows users to query the simulation data within a specified bounding box.  Users can specify timestep
ranges of interest, including the interpolated position of particles within fractional timesteps.

```
python query_simulation.py python <input filename> <left> <right> <top> <bottom> <start time> <end time>
```

# Libraries 
- numpy
- scipy
- matplotlib
