import os
import shutil

# Specify the directory you want to search for .obj files
root_dir = './data/04401088'  # Replace with your root directory path
destination_dir = './ShapeNet/telephone'  # Replace with your destination directory path

# Make sure the destination directory exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Walk through the directory structure
for subdir, _, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.obj'):
            file_path = os.path.join(subdir, file)
            print(f"Found .obj file: {file_path}")

            # Get a unique identifier based on the folder structure (e.g., folder names)
            # Split the subdir path and join it to form part of the new file name
            unique_identifier = "_".join(os.path.relpath(subdir, root_dir).split(os.sep))
            
            # Create a new file name that includes the unique identifier
            new_file_name = f"{unique_identifier}_{file}"
            new_file_path = os.path.join(destination_dir, new_file_name)
            
            # Copy the file and rename it
            shutil.copy(file_path, new_file_path)
            print(f"Copied and renamed {file} to {new_file_name} in {destination_dir}")


# 02828884 - bench 
# 02876657 - bottle
# 04225987 skateboard
# 03046257 - clock 
# 03325088 faucet
# 03593526 jar
# 03642806 laptop
# 03691459 loudspeaker
# 04401088 telephone
