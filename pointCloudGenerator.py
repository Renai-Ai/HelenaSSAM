# import trimesh
# import numpy as np
# import torch
# from torch_geometric.data import Data
# import open3d as o3d

# # Define the file paths
# obj_file_path = './ShapeNet/bench/1a40eaf5919b1b3f3eaa2b95b99dae6_models_model_normalized.obj'  # Replace with your specific file path
# output_file_path = 'sample_point_cloud.ply'  # Save location for the point cloud

# def save_point_cloud(point_cloud, file_path):
#     """Save the point cloud as a .ply file."""
#     pcd = o3d.geometry.PointCloud()
#     pcd.points = o3d.utility.Vector3dVector(point_cloud)
#     o3d.io.write_point_cloud(file_path, pcd)

# def load_obj(file_path):
#     """Load a .obj file and return a PyTorch Geometric Data object."""
#     scene = trimesh.load(file_path)
    
#     # Sample points from the mesh
#     if isinstance(scene, trimesh.Scene):
#         point_cloud = np.vstack([g.sample(1024) for g in scene.geometry.values() if g])
#     else:
#         point_cloud = scene.sample(1024)

#     if point_cloud is not None:
#         data = Data(pos=torch.tensor(point_cloud, dtype=torch.float32))
#         return data
#     else:
#         raise ValueError(f"No point cloud generated for {file_path}")

# def visualize_point_cloud(file_path):
#     """Visualize a point cloud using Open3D."""
#     pcd = o3d.io.read_point_cloud(file_path)
#     o3d.visualization.draw_geometries([pcd])

# # Load and save the point cloud
# import torch_geometric.transforms as T

# # Apply scale normalization after loading
# transform = T.NormalizeScale()

# # After loading, transform the data
# data = load_obj(obj_file_path)
# data = transform(data)  # Normalize the scale

# # data = load_obj(obj_file_path)
# save_point_cloud(data.pos.numpy(), output_file_path)
# print(f"Saved point cloud to {output_file_path}")

# # Visualize the saved point cloud
# visualize_point_cloud(output_file_path)


import os
import glob
import trimesh
import numpy as np
import torch
from torch_geometric.data import Data
import open3d as o3d
import torch_geometric.transforms as T

# Set the directory containing .obj files and output folder for .ply files
input_folder = './ShapeNet/telephone/'  # Folder containing .obj files
output_folder = './PointClouds/telephone'  # Folder to save .ply files

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define the transform to normalize scale
transform = T.NormalizeScale()

def save_point_cloud(point_cloud, file_path):
    """Save the point cloud as a .ply file."""
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(point_cloud)
    o3d.io.write_point_cloud(file_path, pcd)

def load_obj(file_path):
    """Load a .obj file and return a PyTorch Geometric Data object."""
    scene = trimesh.load(file_path)
    
    # Sample points from the mesh
    if isinstance(scene, trimesh.Scene):
        point_cloud = np.vstack([g.sample(1024) for g in scene.geometry.values() if g])
    else:
        point_cloud = scene.sample(1024)

    if point_cloud is not None:
        data = Data(pos=torch.tensor(point_cloud, dtype=torch.float32))
        return data
    else:
        raise ValueError(f"No point cloud generated for {file_path}")

def visualize_point_cloud(file_path):
    """Visualize a point cloud using Open3D."""
    pcd = o3d.io.read_point_cloud(file_path)
    o3d.visualization.draw_geometries([pcd])

# Process all .obj files in the input folder
obj_files = glob.glob(os.path.join(input_folder, '*.obj'))

for obj_file_path in obj_files:
    # Load and transform the point cloud
    data = load_obj(obj_file_path)
    data = transform(data)  # Normalize the scale

    # Save the point cloud to a .ply file
    file_name = os.path.splitext(os.path.basename(obj_file_path))[0]  # Get file name without extension
    output_file_path = os.path.join(output_folder, f"{file_name}.ply")
    save_point_cloud(data.pos.numpy(), output_file_path)
    print(f"Saved point cloud to {output_file_path}")

    # Visualize the saved point cloud
    #visualize_point_cloud(output_file_path)
