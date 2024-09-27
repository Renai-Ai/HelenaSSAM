import os
import json
import yaml

# Define the paths to the required datasets
deepcad_path = r'C:/Users/Manik/Downloads/DeepCAD Dataset/cad_json'
abc_dataset_path = r'C:/Users/Manik/Downloads/ABC Dataset'
combined_dataset_path = r'C:/Users/Manik/Downloads/Combined Dataset'

# Iterate through all subfolders in the DeepCAD Dataset
for deepcad_folder in os.listdir(deepcad_path):
    deepcad_folder_path = os.path.join(deepcad_path, deepcad_folder)
    
    # Skip if not a folder
    if not os.path.isdir(deepcad_folder_path):
        continue

    # Corresponding folder in the ABC Dataset
    abc_folder_name = f"abc_{deepcad_folder}_meta_v00"
    abc_folder_path = os.path.join(abc_dataset_path, abc_folder_name)

    # Skip if the corresponding ABC folder does not exist
    if not os.path.exists(abc_folder_path):
        continue

    # Iterate through JSON files in the current DeepCAD folder
    for json_file in os.listdir(deepcad_folder_path):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(deepcad_folder_path, json_file)

            # Extract the base name to find the corresponding folder in ABC Dataset
            base_name = json_file.replace('.json', '')
            abc_subfolder_path = os.path.join(abc_folder_path, base_name)

            # Check if the corresponding subfolder exists in ABC Dataset
            if not os.path.exists(abc_subfolder_path):
                continue

            # Look for the YAML file in the ABC subfolder
            for yml_file in os.listdir(abc_subfolder_path):
                if yml_file.endswith('.yml'):
                    yml_file_path = os.path.join(abc_subfolder_path, yml_file)

                    # Read the YAML file and extract the 'name' field
                    with open(yml_file_path, 'r') as file:
                        try:
                            yml_data = yaml.safe_load(file)
                            name_value = yml_data.get('name', 'Unnamed')

                            # Read the corresponding JSON file from DeepCAD
                            with open(json_file_path, 'r') as json_f:
                                json_data = json.load(json_f)

                            # Add the 'name' field to the JSON data
                            json_data['name'] = name_value

                            # Create the required folder structure in the Combined Dataset
                            combined_subfolder_path = os.path.join(combined_dataset_path, deepcad_folder)
                            os.makedirs(combined_subfolder_path, exist_ok=True)

                            # Create the new JSON file path within the same folder structure
                            new_json_file_name = f"{base_name}_combined.json"
                            output_file_path = os.path.join(combined_subfolder_path, new_json_file_name)

                            # Write the modified JSON to the Combined Dataset folder
                            with open(output_file_path, 'w') as output_f:
                                json.dump(json_data, output_f, indent=4)

                            print(f"Processed and saved: {output_file_path}")

                        except yaml.YAMLError as exc:
                            print(f"Error reading YAML file {yml_file_path}: {exc}")
