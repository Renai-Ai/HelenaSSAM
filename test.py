import trimesh
import numpy as np
import os
import pickle  # to save voxel grids as binary files

def voxelize_obj(file_path, voxel_size=0.1):
    # Load the mesh from the .obj file
    mesh = trimesh.load(file_path)

    # Calculate bounds and grid shape
    min_bounds = mesh.bounds[0]
    max_bounds = mesh.bounds[1]
    grid_shape = np.ceil((max_bounds - min_bounds) / voxel_size).astype(int)
    
    # Create a grid to store voxel data
    voxel_grid = np.zeros(grid_shape, dtype=bool)

    # Voxelize the mesh
    for x in range(grid_shape[0]):
        for y in range(grid_shape[1]):
            for z in range(grid_shape[2]):
                voxel_center = min_bounds + np.array([x, y, z]) * voxel_size
                
                # Check if voxel center is inside the mesh
                # if mesh.contains([voxel_center]):
                #     voxel_grid[x, y, z] = True

    return voxel_grid

def process_folder(input_folder, output_folder, voxel_size=0.1):
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each .obj file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".obj"):
            file_path = os.path.join(input_folder, filename)
            voxel_grid = voxelize_obj(file_path, voxel_size=voxel_size)
            
            # Save the voxel grid
            output_path = os.path.join(output_folder, filename.replace(".obj", ".pkl"))
            with open(output_path, 'wb') as f:
                pickle.dump(voxel_grid, f)
            
            print(f"Saved voxelized grid for {filename} to {output_path}")

# Example usage:
input_folder = './ShapeNet/bench'
output_folder = './VoxelizedShapes/bench'
process_folder(input_folder, output_folder, voxel_size=0.1)
