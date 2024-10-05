import os
import json
import numpy as np
import logging
import h5py
from joblib import Parallel, delayed
import sys
sys.path.append("..")
from cadlib.extrude import CADSequence
from cadlib.macro import *

# Define a dictionary to map shape types to their parameter indices
SHAPE_PARAMETERS = {
    0: [1, 2],  # Line: x, y (end-point)
    1: [1, 2, 3, 4],  # Arc: x, y (end-point), α (sweep angle), f (counter-clockwise flag)
    2: [1, 2, 5],  # Circle: x, y (center), r (radius)
    5: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],  # Extrude: θ, φ, γ, px, py, pz, s, e1, e2, b, u
    3: [],  # End of Shape, no parameters
    4: [],  # Start of loop
}

DATA_ROOT = "CADvec"
RAW_DATA = os.path.join(DATA_ROOT, "cad_json")
RECORD_FILE = os.path.join(DATA_ROOT, "train_val_test_split.json")

SAVE_DIR = os.path.join(DATA_ROOT, "cad_vec_noise")
logging.basicConfig(filename="noise_changes.log", level=logging.INFO)
print(SAVE_DIR)
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_shape_type(number):
    """Return the shape type number."""
    return SHAPE_PARAMETERS.get(number, [])

def is_discrete(value):
    """Check if a value is discrete (no significant decimal portion)."""
    if isinstance(value, np.ndarray):
        return np.all(np.isclose(value, np.round(value), atol=1e-8))
    return np.isclose(value, np.round(value), atol=1e-8)

# def add_noise(vector, noise_level=1):
#     """Add noise to continuous values in the vector."""
#     noisy_vector = vector.copy()
#     for i in range(len(noisy_vector)):
#         for j in range(len(noisy_vector[i])):
        
#             noisy_vector[i][j] += np.random.normal(0, noise_level)
            
#             # else:
#             #     print(f"Discrete value at index {i}, {j}: {noisy_vector[i][j]}")
#     return noisy_vector

def add_noise(vector, noise_level=0.1):
    noisy_vector = vector.copy()
    for i in range(len(noisy_vector)):
        # Get the shape type of the current shape
        shape_type = noisy_vector[i][0] #the first element of the vector
        #get the noise indicis for the shape type
        noise_indices = get_shape_type(shape_type)
        print(f"Noise indices for shape type {shape_type}: {noise_indices}")
        for j in noise_indices:
            noisy_vector[i][j] += np.random.normal(0, noise_level)

    return noisy_vector

def process_one(data_id):
    json_path = os.path.join(RAW_DATA, data_id + ".json")
    with open(json_path, "r") as fp:
        data = json.load(fp)

    try:
        cad_seq = CADSequence.from_dict(data)
        cad_seq.normalize()
        cad_seq.numericalize()
        cad_vec = cad_seq.to_vector(MAX_N_EXT, MAX_N_LOOPS, MAX_N_CURVES, MAX_TOTAL_LEN, pad=False)

    except Exception as e:
        print("failed:", data_id)
        return

    if MAX_TOTAL_LEN < cad_vec.shape[0] or cad_vec is None:
        print("exceed length condition:", data_id, cad_vec.shape[0])
        return
    
    print(f"Original vector for {data_id}: {cad_vec}")
    # Here is where we add noise to the dataset 
    noisy_cad_vec = add_noise(cad_vec) 
    print(f"Noisy vector for {data_id}: {noisy_cad_vec}")

    diff = noisy_cad_vec - cad_vec
    print(f"Difference after adding noise for {data_id}: {diff}")

    logging.info(f"Original vector for {data_id}: {cad_vec}")
    logging.info(f"Noisy vector for {data_id}: {noisy_cad_vec}")
    logging.info(f"Difference after adding noise for {data_id}: {diff}")

    # Save path with noisy identifier in the filename
    save_path = os.path.join(SAVE_DIR, data_id + "_noisy.h5")
    truck_dir = os.path.dirname(save_path)
    if not os.path.exists(truck_dir):
        os.makedirs(truck_dir)

    with h5py.File(save_path, 'w') as fp:
        fp.create_dataset("vec", data=noisy_cad_vec, dtype=np.float32)

with open(RECORD_FILE, "r") as fp:
    all_data = json.load(fp)

Parallel(n_jobs=10, verbose=2)(delayed(process_one)(x) for x in all_data["train"])
Parallel(n_jobs=10, verbose=2)(delayed(process_one)(x) for x in all_data["validation"])
Parallel(n_jobs=10, verbose=2)(delayed(process_one)(x) for x in all_data["test"])


