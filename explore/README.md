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


# JSON to Blender Readable Python

## Overview

This project aims to convert JSON data into Blender-readable Python scripts, facilitating the manipulation and visualization of 3D objects in Blender. The toolset currently includes functionalities for extruding objects, mirroring them, rotating, translating, and creating lines and arcs.

## Toolset

### Tool 1: Extrude Object (4.5 Hours)

**IDEA:**  
Similar to the extrude function in Blender’s UI, this tool allows the user to extrude an object from its original shape along specified parameters.

**PROGRESS:**  
- Explored Blender’s interface and determined that extrusions can only be performed in Edit Mode.
- Implemented the extrude operation using `bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":extrude_vector})`.
- Supported extrusion along any axis, based on user-defined parameters.
- Initially tested on a cube, which worked as expected.
- Noted issues with curvatures on objects like cones, which resulted in polygon-like shapes.
- Developed a function to smooth surfaces based on curvature detection, which successfully smoothed cones but caused planes to turn black due to normals issues.
- Suggested providing users with an option to smooth shapes, preventing black coloration on plane-like shapes.
- Successfully tested negative extrusion amounts and all axis options (X, Y, Z).

**ISSUES:**  
- Black plane issue after smoothing operations.

---

### Tool 2: Mirror (4 Hours)

**IDEA:**  
To symmetrically duplicate an object across a user-defined axis, similar to a mirror effect.

**PROGRESS:**  
- Gained familiarity with Blender’s interface, enabling more confident tool development.
- Initially attempted mirroring with `bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(True, False, False))` but encountered issues with irregular shapes.
- Researched and discovered that mirroring should be performed through modifiers.
- Successfully created a mirror modifier instance and tested it on an irregular shape, achieving the desired result.
- Explored the idea of mirroring across a custom axis but faced execution challenges, requiring further research.

**ISSUES:**  
- Custom axis mirroring needs additional attention.

---

### Tool 3: Rotation (1 Hour)

**IDEA:**  
To rotate an object by 'n' degrees counterclockwise around any specified axis.

**PROGRESS:**  
- Implemented rotation using `obj.rotation_euler[0] += radians(angle)` and successfully matched the axis to user parameters.
- Tested various cases, including all axes, negative degree inputs, zero degree inputs, and rational number inputs, all functioning as expected.

**ISSUES:**  
- None reported.

---

### Tool 4: Translating (1 Hour)

**IDEA:**  
To translate the object a specified number of units along a user-defined direction.

**PROGRESS:**  
- Used `obj.location.x += translation_amount` to implement translation.
- Followed similar testing procedures as the rotation tool (including all axes, negative unit inputs, zero unit inputs, and rational number inputs), resulting in expected outcomes.

**ISSUES:**  
- None reported.

---

### Tool 5: Create Line and Create Arc (2 Hours)

**IDEA:**  
To create basic geometric shapes based on the JSON object data.

**PROGRESS:**  
- Developed functionality to create a line using extracted start and end points from the JSON object.
- Implemented an arc creation function, utilizing center coordinates, radius, start angle, and end angle from the JSON data.

---

### Processing the JSON (3 Hours)

**IDEA:**  
To identify and map entities, properties, and types within the JSON structure to their corresponding Blender elements.

**PROGRESS:**  
- Faced challenges in understanding the JSON structure and its correlation to Blender’s mesh manipulation.
- Focused on identifying profiles in the JSON data, outlining the logic needed to combine these with transformations for the final output.
- Completed the profiles mapping and developed a generic understanding of the overall logic.

---

## Future Improvements

- Address the black plane issue during the smoothing process.
- Enhance custom axis mirroring functionality.
- Continue refining the JSON processing logic for more complex shapes and transformations.
