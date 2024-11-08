import bpy
import os

# Specify your ShapeNet model directory and output directory
model_dir = './data/02828884'
output_dir = './2D/bench'

# Camera positions for different views
views = [
    (1.0, 0.0, 0.5),
    (-1.0, 0.0, 0.5),
    (0.0, 1.0, 0.5),
    (0.0, -1.0, 0.5),
]

# Loop through each model file
for model_file in os.listdir(model_dir):
    if model_file.endswith(".obj"):  # Adjust if needed based on model filetype
        model_path = os.path.join(model_dir, model_file)
        bpy.ops.import_scene.obj(filepath=model_path)
        
        for i, view in enumerate(views):
            # Set up the camera
            bpy.context.scene.camera.location = view
            bpy.context.scene.camera.rotation_euler = (0, 0, 0)
            
            # Render the scene
            output_path = os.path.join(output_dir, f"{model_file}_{i}.png")
            bpy.context.scene.render.filepath = output_path
            bpy.ops.render.render(write_still=True)
        
        # Delete the model to prepare for the next iteration
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':  # Adjust if needed based on model type
                obj.select_set(True)
        bpy.ops.object.delete(use_global=False)

        # Optionally clean up unused data blocks
        # This can help free up memory as well
        for material in bpy.data.materials:
            if material.users == 0:
                bpy.data.materials.remove(material)

# You can also clear out any collections or other unused data as needed
