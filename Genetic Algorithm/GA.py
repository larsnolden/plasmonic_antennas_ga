import numpy as np
import pygad as pg
import os.path
import pandas as pd
from datetime import datetime

# mnonkeypatch replacement of cloudpickle with dill
# as cloudpickle would lead to errors when restarting 
# from a savepoint due to multiprocessing class issues (?)
import dill
import sys
#sys.modules['pickle'] = dill
sys.modules['cloudpickle'] = dill

from comsolClient import runSimulation
from generateCurveAndHoles import generateCurve

SAVEPOINT_FILE_NAME = "ga_savepoint"
MESH_RESOLUTION = "coarse"
SOLUTIONS_CSV_PATH = './solutions.csv'

def generate_antenna_name(image_representation):
    # remove all array formatting and only retain the Boolean values
    return (
        str(image_representation.flatten())
        .replace("\n", "")
        .replace(" ", "")
        .replace("[", "")
        .replace("]", "")
    )


def fitness(ga_instance, solution, solution_idx):
    global solutions
    global MESH_RESOLUTION

    print(f"solution_idx: {solution_idx}")
    if solution.max() == 0:
        # return low fitness if solution is empty (all zeros)
        return 0

    try:
        # avoid crashing the program if there are errors in the simulation
        image_representation = solution.reshape(11, 11)
        antenna_name = generate_antenna_name(image_representation)

        outer_contour_file_path, inner_contour_file_path = generateCurve(
            image_representation,
            padding=100,
            image_path=f"./images/{antenna_name}.png",
            antenna_name=antenna_name,
        )
        # run simulation
        fitness = runSimulation(
            inner_contour_file_path=inner_contour_file_path,
            outer_contour_file_path=outer_contour_file_path,
            mesh_resolution=MESH_RESOLUTION,
            model_path=f"./models/{antenna_name}.mph",
        )

        # record all solutions
        now = datetime.now()
        date_time = now.strftime("%d.%m.%Y, %H:%M:%S")

            # create or load solutions file in fitness function to support multiprocessing
        try:
            # load existing solutions file if exists
            solutions = pd.read_csv(SOLUTIONS_CSV_PATH, index_col=0)
        except FileNotFoundError: 
            # create solutions df
            solutions = pd.DataFrame(
                columns=["fitness", "solution", "computed_on", "generation", "mesh-resoution"]
            )
        new_row = pd.DataFrame(
            [
                [
                    fitness,
                    str(solution),
                    date_time,
                    ga_instance.generations_completed,
                    MESH_RESOLUTION,
                ]
            ],
            columns=solutions.columns,
        )
        # concat new data to solutions csv
        solutions = pd.concat([solutions, new_row], ignore_index=True)
        solutions.to_csv(SOLUTIONS_CSV_PATH)
        
        ga_instance.save(SAVEPOINT_FILE_NAME)  # save progress on each solution
        print("Generation : ", ga_instance.generations_completed)
        return fitness
    except OSError as e:
        # out of disk space
        print(e)
        return fitness  # still compute fitness
    except Exception as e:
        print("Exception occured, returning 0 fitness")
        print(e)
        return 0


dim = 11 * 11

ga_instance = pg.GA(
    num_generations=400,
    num_parents_mating=15,  # num parents from each generation choosen that produce all of the new generation offspring
    fitness_func=fitness,
    sol_per_pop=40,
    num_genes=dim,
    init_range_low=0,
    init_range_high=2,  # exclusive
    parent_selection_type="rank",  # rank: select parents based on their fitness ranking
    keep_elitism=4,  # keep the best 4 parents
    gene_type=int,
    crossover_type="uniform",  # uniform: choose either parent bit with the same probability
    mutation_percent_genes=4,
    parallel_processing=["process", 1],  # use x processes
    # save_best_solutions=True,  # best solution after each generation is saved into an attribute named best_solution
    # save_solutions=True,  # all solutions after each generation are saved into an attribute named solutionss
)


if __name__ == "__main__":
    # check if there is a savepoint
    savepoint_file_exists = os.path.isfile(f"{SAVEPOINT_FILE_NAME}.pkl")
    if savepoint_file_exists:
        # overwrite the default ga_instance with the saved one
        print("Savepoint found, resuming from savepoint")
        ga_instance = pg.load(SAVEPOINT_FILE_NAME)
    else:
        print("No savepoint found, starting from scratch")

    ga_instance.run()
