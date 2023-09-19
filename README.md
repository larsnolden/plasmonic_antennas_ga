## Genetic Algorithm to create nano-plasmonic antennas

A genetic algorithm that generates nano-plasmonic antenna designs with the goal to maximize the light induced heat generation. Utilizes Comsol FEM simulation for fitness evaluation.
This code is the result of my [bachelor thesis](genetic_algorithm_plasmonic_antennas__Lars_Nolden_2600854_Bachelor_Thesis.pdf).

## Get Started

The `Genetic Algorithm` folder contains all relevant files to run the algorithm.
Start a new simulation by running `python GA.py`.
The algorithm will generate new contour, image and model files.
Genetic algorithm parameters can be adjustedn in `GA.py`.
The file `generateCurveAndHoles.py` generates the inner and outer contours from an antenna image.
Those files are saved in the `/contours` folders and imported into Comsol to form the geometry. Where the inner contours are used to represent holes in the geometry.
The file `comsolClient.py` uses the `mph` python library to connect to a comsol instance (You are not required to have a Comsol window open for this). And builds the entire model via the Comsol API. The final model output is saved in the `/models` folder. Such that all simulations are saved and do not have to be rerun if other simulation result data is necessary after the fact.
A `solutions.csv` file is generated that contains each antennas fitness and it's representation in binary string format. This file is the main source of information used in the analysis.

## Analysis

Four Jupyter notebooks are included. The `frequency_sweep.ipynb` processes a CSV export of a frequency sweep in comsol and creates a nice looking graph.
The `correlations.ipynb` analyses the correlation between the antenna surface area, island count and the antennas performance.
The `/solutions` folder contains the `convergence.ipynb` that renders a graph comparing two different algorithm runs comparing the convergence (or lack there of) for different genetic algorithm parameters.
It also contains the `solutions_analysis.ipynb` notebook which gives information about the best candidates and their performance. Further a heatmap of all antennas pixels and their normalized fitness is created. This indicates which pixels are more likely to be associated with a 'good' performing antenna.
