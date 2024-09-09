# JSON to .STL

This script processes CAD models stored in `h5` or `json` format and exports them as STL files. The OpenCASCADE library was utilized for data exchange and for validating CAD models, ensuring that only accurate and error-free models are exported.

## Requirements

1. **Install Requirements from DeepCAD GitHub**

   This script depends on the DeepCAD library. Please refer to the [DeepCAD GitHub repository](https://github.com/ChrisWu1997/DeepCAD) for instructions on how to install the required dependencies.


# Usage
To generate the .stl files from JSON please run the following:  \

```python
python .\export2stl.py --src <source-folder> --form <file_format> --outputs <output-folder>
```
-- `src <source_folder>`: The path to the folder containing input files. This argument is required.\
--`form <file_format>`: The format of the input files. Options are h5 or json. \
--`outputs <output_folder>`: The folder where the STL files will be saved.


# Importing STL Files into Blender
Once the STL files are generated, you can import them into Blender for further visualization or editing:

1. Open Blender. 
2. Go to `File > Import > STL`. 
3. Select the STL files you want to import. 

Note: You may need to install the STL file import extension for Blender if it's not already available. You can download and install it through Blender's preferences.

# Check with `show.py`

After running the script, you can use show.py to verify and visualize the generated STL files. Run the following command to check the files:

```python
python show.py --src <source-folder> --form <file_format>
```

-- `src <source_folder>`: The path to the folder containing input files. This argument is required.\
--`form <file_format>`: The format of the input files. Options are h5 or json. 



