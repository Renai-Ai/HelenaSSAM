import os
import glob
import json
import bpy
import bmesh
import math
from math import radians
import h5py
import numpy as np
from OCC.Display.SimpleGui import init_display
from OCC.Core.gp import gp_Vec, gp_Trsf
from OCC.Core.TopLoc import TopLoc_Location
from OCC.Core.BRepCheck import BRepCheck_Analyzer
import argparse
import sys
sys.path.append("..")
from cadlib.extrude import CADSequence
from cadlib.visualize import vec2CADsolid, create_CAD


parser = argparse.ArgumentParser()
parser.add_argument('--src', type=str, required=True, help="source folder")
parser.add_argument('--form', type=str, default="h5", choices=["h5", "json"], help="file format")
parser.add_argument('--idx', type=int, default=0, help="show n files starting from idx.")
parser.add_argument('--num', type=int, default=10, help="number of shapes to show. -1 shows all shapes.")
parser.add_argument('--with_gt', action="store_true", help="also show the ground truth")
parser.add_argument('--filter', action="store_true", help="use opencascade analyzer to filter invalid model")
args = parser.parse_args()

src_dir = args.src
print(src_dir)
out_paths = sorted(glob.glob(os.path.join(src_dir, "*.{}".format(args.form))))
if args.num != -1:
    out_paths = out_paths[args.idx:args.idx+args.num]


def extrude_object(obj, amount, axis, smooth=True):
#I believe
    # Ensure the object exists
    obj = bpy.data.objects.get(obj)
    if obj is None:
        raise ValueError(f"Object '{obj}' not found.")
#    
#    # Select the object
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    
    # Ensure we're in Object Mode
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Switch to Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Select all faces
    bpy.ops.mesh.select_all(action='SELECT')
    
    extrude_vector = {
        'X': (amount, 0, 0),
        'Y': (0, amount, 0),
        'Z': (0, 0, amount)
    }.get(axis.upper(), (0, 0, 0))
    

    # Extrude the selected faces
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":extrude_vector})
    
   
    bpy.ops.object.mode_set(mode='OBJECT')
    #needs to be in object mode to perform smooth
    
    if smooth:
        bpy.ops.object.shade_smooth()

    bpy.ops.object.mode_set(mode='OBJECT')


def mirror_object(obj, axis, custom_axis=None):
#works for axis X Y Z but I am not sure about custom axis


    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

 
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
  
    obj = bpy.context.object

    # Add a mirror modifier
    mirror_modifier = obj.modifiers.new(name="Mirror", type='MIRROR')
    
    # Standard axis mirroring
    if custom_axis is None:
        if axis == 'Y':
            #bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(True, False, False))
            mirror_modifier.use_axis[0] = True
            mirror_modifier.use_axis[1] = False # Y-axis
            mirror_modifier.use_axis[2] = False # Z-axis
        elif axis == 'X':
            mirror_modifier.use_axis[0] = False
            mirror_modifier.use_axis[1] = True # Y-axis
            mirror_modifier.use_axis[2] = False # Z-axis
        elif axis == 'Z':
            #bpy.ops.transform.mirror(orient_type='GLOBAL', constraint_axis=(False, False, True))
            mirror_modifier.use_axis[0] = False
            mirror_modifier.use_axis[1] = False # Y-axis
            mirror_modifier.use_axis[2] = True # Z-axis
        else:
            
            # Create a custom mirror matrix using the custom axis
            axis_vector = custom_axis.normalized()  # Normalize the custom axis
            mirror_matrix = mathutils.Matrix.Scale(-1.0, 4, axis_vector)
        
       # Apply the modifier (optional)
    bpy.ops.object.modifier_apply(modifier="Mirror")

    
    # Update the scene to reflect changes
    bpy.context.view_layer.update()
    
    return obj



def rotate_object(obj, axis, angle):
    
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

 
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
  
    obj = bpy.context.object
    
    # Ensure valid input for axis
    if axis not in ['X', 'Y', 'Z']:
        raise ValueError("Invalid axis! Use 'X', 'Y', or 'Z'.")
    
    # Rotate the object based on the specified axis
    if axis == 'X':
        obj.rotation_euler[0] += radians(angle)  # Rotate around X-axis
    elif axis == 'Y':
        obj.rotation_euler[1] += radians(angle)  # Rotate around Y-axis
    elif axis == 'Z':
        obj.rotation_euler[2] += radians(angle)  # Rotate around Z-axis
    
    # Update the scene to apply the rotation
    bpy.context.view_layer.update()
    
    return obj


def create_line(start, end):
    """Creates a line mesh between two points and adds it to the scene."""
    mesh = bpy.data.meshes.new("line_mesh")
    obj = bpy.data.objects.new("Line", mesh)
    bpy.context.collection.objects.link(obj)
    
    mesh.from_pydata([start, end], [(0, 1)], [])
    mesh.update()
    
    return obj

def create_arc(center, radius, start_angle, end_angle, resolution=32):
    """Creates an arc mesh between two angles and adds it to the scene."""
    mesh = bpy.data.meshes.new("arc_mesh")
    obj = bpy.data.objects.new("Arc", mesh)
    bpy.context.collection.objects.link(obj)
    
    verts = []
    edges = []
    
    # Convert the center point to a tuple
    center_tuple = (float(center[1]), float(center[0]), float(center[2]))
    
    step = (end_angle - start_angle) / resolution
    for i in range(resolution + 1):
        angle = start_angle + step * i
        x = center_tuple[0] + radius * math.cos(angle)
        y = center_tuple[1] + radius * math.sin(angle)
        z = center_tuple[2]
        verts.append((x, y, z))
        if i > 0:
            edges.append((i - 1, i))
    
    mesh.from_pydata(verts, edges, [])
    mesh.update()
    
    return obj

def translate_object(obj, translation_amount, direction):
    # Get the object by name
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

 
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
  
    #obj = bpy.context.object

   
            # Translate based on direction input
    if direction.lower() == 'x':
        obj.location.x += translation_amount
        
    elif direction.lower() == 'y':
        obj.location.y += translation_amount
       
    elif direction.lower() == 'z':
        obj.location.z += translation_amount
        
    else:
        print(f"Invalid direction: {direction}. Use 'x', 'y', or 'z'.")
#    else:
#        print(f"Object {object_name} not found.")
            
    return obj


def scale_obj(obj, X_scale, Y_scale, Z_scale):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

 
    if bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')
        
    obj.scale = (X_scale, Y_scale, Z_scale)
    
    bpy.ops.object.transform_apply(location = False, rotation = False, scale = True)
    
    return obj

def combine_objects(objects, name):
    # Ensure the objects exist
    for obj in objects:
        if bpy.data.objects.get(obj) is None:
            raise ValueError(f"Object '{obj}' not found.")
    
    # Select all objects
    for obj in objects:
        bpy.data.objects[obj].select_set(True)
        #obj.select_set(True) not sure if this is correct or the other
    
    # Make the first object the active object
    bpy.context.view_layer.objects.active = objects[0]

    # Combine the objects
    bpy.ops.object.join()
    
    # Rename the object
    bpy.context.object.name = name
    
    return bpy.context.object

def read_json(json_file_path):
    try:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)  # Parse the JSON data
            return data
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
    
    
def process_json_file(json_file_path):
    json_data = read_json(json_file_path)
    if json_data:
        process_json(json_data)

def process_profiles(profiles):
    profiles_created = {}
    
    for i in range(0, len(profiles)):
        # Get the profile type
        profile_name = profiles[i]
        for loop in profiles['loops']:
            temp_created = {}
            for curve in loop['profile_curves']:
                
                curve_type = curve['type']

                if curve_type == 'Line3D':
                    #get the start and end points
                    start = curve['start_point']
                    end = curve['end_point']

                    obj = create_line(start, end)
                    temp_created[profile_name] = obj

                elif curve_type == 'Arc3D':
                    center = curve['center_point']
                    radius = curve['radius']
                    start_angle = curve['start_angle']
                    end_angle = curve['end_angle']
                    obj = create_arc(center, radius, start_angle, end_angle)
                    temp_created[profile_name] = obj
            
            combined_obj = combine_objects(temp_created, profile_name)
            profiles_created[profile_name] = combined_obj
    
    return profiles_created

#we have all these profiles and we know that they belong to a certain entity 
#now lets see if we can apply the transformations to the profiles

def apply_transformations(entity_data, entity_id, entity_type):
    # Get the entity's transformation data
    transformation_data = entity_data['transformation']
    
    # Get the entity's profiles
    profiles = entity_data['profiles']
    
    # # Process the profiles
    # profiles_created = process_profiles(profiles)
    
    # # Apply the transformations to the profiles
    # for profile_name, profile_obj in profiles_created.items():
    #     # Get the transformation data for the profile
    #     profile_transformation_data = transformation_data[profile_name]
        
    #     # Apply the transformations to the profile
    #     profile_obj = apply_transformation(profile_obj, profile_transformation_data)
    
    # # Combine the profiles
    # combined_obj = combine_objects(profiles_created.values(), entity_id)
    
    # return combined_obj

def process_json(data):
    if data is None: 
        print("Error: No data found.")
        return
    #now let us go through the sequence first 

    objects_created = {}

    for sq in data['sequence']: 
        print(sq)
        print(sq['type'])
        entity_id = sq['entity']
        entity_type = sq['entity_type']
        entity_data = data['entities'][entity_id]

        if entity_type == 'ExtrudeFeature':
            print(f"Processing extrusion for entity: {entity_id}")
            #get the sketch obkect that is being extruded 
            sketch_data = entity_data['profiles'][0]
            obj = sq['object']
            amount = sq['amount']
            axis = sq['axis']
            smooth = sq['smooth']
            extrude_object(obj, amount, axis, smooth)
            objects_created[obj] = bpy.data.objects[obj]
    
        

            
