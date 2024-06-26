import bpy
import math
import sys
import os
import numpy

#upd position points
'''
max_middle_poin = (-0.049776, -1.3417, 6.7215)
min_middle_poin = (-0.049775, -3.5286, 2.9707)


#thickness
thickness = sys.argv[7]
th = float(thickness)


#choose X lenght
#leng  = sys.argv[8]
#len = float(leng)

#choose Y lenght
#soly = sys.argv[7]
#sol = float(soly)

#choose number of count 
number = sys.argv[6]
count = int(number)


#set number of count
bpy.data.node_groups["Geometry Nodes.001"].nodes["Resample Curve"].inputs[2].default_value = count

#sol
#bpy.context.object.modifiers["GeometryNodes"]["Socket_3"][1] = sol

#len
#bpy.context.object.modifiers["GeometryNodes"]["Socket_3"][0] = len

'''
#if need run script in Blender
bpy.ops.import_scene.gltf(filepath="C:\\Python\\test\\test_p_3.glb")

'''
#choose file
file_path = sys.argv[5]
bpy.ops.import_scene.gltf(filepath=file_path)
'''

#rename file 
object_to_rename = bpy.context.active_object
object_to_rename.name = "Strap"

#delete coordinate
object_to_delete = bpy.data.objects.get("Strap")

bpy.data.objects.remove(object_to_delete, do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')

objects = bpy.context.scene.objects

#choose parent object to join
parent_object = bpy.data.objects["Plane"]


for obj in objects[1:]:
    obj.select_set(True)


bpy.context.view_layer.objects.active = parent_object
bpy.ops.object.join()

#set pivot point and position 3d model
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')

object_to_rotate = bpy.context.active_object 

#rotate model 
object_to_rotate.rotation_euler[0] += math.radians(90)

#resize
bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

objects = bpy.context.scene.objects

#remove extra triangle
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.tris_convert_to_quads()
bpy.ops.object.editmode_toggle()


#solidify
bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = 0.2
bpy.ops.object.modifier_apply(modifier="Solidify")

#bevel
bpy.ops.object.modifier_add(type='BEVEL')
bpy.context.object.modifiers["Bevel"].segments = 5
bpy.ops.object.modifier_apply(modifier="Bevel")


#choose object in Geometry Nodes
bpy.data.node_groups["Geometry Nodes.001"].nodes["Object Info"].inputs[0].default_value = bpy.data.objects["Plane"]

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

#convert all scene in Mesh (bezie -> mesh)
bpy.ops.object.convert(target='MESH')


#delete Plane befor export
object_name = "Plane" 
object_to_delete = bpy.data.objects.get(object_name)

bpy.data.objects.remove(object_to_delete, do_unlink=True)


#add atribute point
obj = bpy.data.objects["Curve"]

# Установите объект как активный
bpy.context.view_layer.objects.active = obj


"""
See YouTube tutorial here: https://youtu.be/Is8Qu7onvzM
"""

import random
import time

import bpy


################################################################
# helper functions BEGIN
################################################################


def purge_orphans():
    """
    Remove all orphan data blocks

    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    else:
        # run this only for Blender versions lower than 3.0
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()


def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene

    Checkout this video explanation with example

    "How to clean the scene with Python in Blender (with examples)"
    https://youtu.be/3rNqVPtbhzc
    """
    # make sure the active object is not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    # make sure non of the objects are hidden from the viewport, selection, or disabled
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # select all the object and delete them (just like pressing A + X + D in the viewport)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # find all the collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # in the case when you modify the world shader
    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()


def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object


def time_seed():
    """
    Sets the random seed based on the time
    and copies the seed into the clipboard
    """
    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)

    # add the seed value to your clipboard
    bpy.context.window_manager.clipboard = str(seed)

    return seed


def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"


def create_data_animation_loop(obj, data_path, start_value, mid_value, start_frame, loop_length, linear_extrapolation=True):
    """
    To make a data property loop we need to:
    1. set the property to an initial value and add a keyframe in the beginning of the loop
    2. set the property to a middle value and add a keyframe in the middle of the loop
    3. set the property the initial value and add a keyframe at the end of the loop
    """
    # set the start value
    setattr(obj, data_path, start_value)
    # add a keyframe at the start
    obj.keyframe_insert(data_path, frame=start_frame)

    # set the middle value
    setattr(obj, data_path, mid_value)
    # add a keyframe in the middle
    mid_frame = start_frame + (loop_length) / 2
    obj.keyframe_insert(data_path, frame=mid_frame)

    # set the end value
    setattr(obj, data_path, start_value)
    # add a keyframe in the end
    end_frame = start_frame + loop_length
    obj.keyframe_insert(data_path, frame=end_frame)

    if linear_extrapolation:
        set_fcurve_extrapolation_to_linear()


def set_scene_props(fps, frame_count):
    """
    Set scene properties
    """
    scene = bpy.context.scene
    scene.frame_end = frame_count

    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1


def scene_setup():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()

    clean_scene()

    set_scene_props(fps, frame_count)


################################################################
# helper functions END
################################################################


def link_nodes_by_mesh_socket(node_tree, from_node, to_node):
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Mesh"])


def create_node(node_tree, type_name, node_x_location, node_location_step_x=0):
    """Creates a node of a given type, and sets/updates the location of the node on the X axis.
    Returning the node object and the next location on the X axis for the next node.
    """
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_x_location
    node_x_location += node_location_step_x

    return node_obj, node_x_location


def update_geo_node_tree(node_tree):
    """
    Adding a Cube Mesh, Subdiv, Triangulate, Edge Split, and Element scale geo node into the
    geo node tree

    Geo Node type names found here
    https://docs.blender.org/api/current/bpy.types.GeometryNode.html
    """


    #подключение к крайней ноде
    out_node = node_tree.nodes["Group Output"]

    node_x_location = 0
    node_location_step_x = 300

    mesh_cube_node, node_x_location = create_node(node_tree, "GeometryNodeMeshCube", node_x_location, node_location_step_x)

    subdivide_mesh_node, node_x_location = create_node(node_tree, "GeometryNodeSubdivideMesh", node_x_location, node_location_step_x)
    subdivide_mesh_node.inputs["Level"].default_value = 3

    triangulate_node, node_x_location = create_node(node_tree, "GeometryNodeTriangulate", node_x_location, node_location_step_x)

    split_edges_node, node_x_location = create_node(node_tree, "GeometryNodeSplitEdges", node_x_location, node_location_step_x)

    scale_elements_node, node_x_location = create_node(node_tree, "GeometryNodeScaleElements", node_x_location, node_location_step_x)
    scale_elements_node.inputs["Scale"].default_value = 0.8

    out_node.location.x = node_x_location

    link_nodes_by_mesh_socket(node_tree, from_node=mesh_cube_node, to_node=subdivide_mesh_node)
    link_nodes_by_mesh_socket(node_tree, from_node=subdivide_mesh_node, to_node=triangulate_node)
    link_nodes_by_mesh_socket(node_tree, from_node=triangulate_node, to_node=split_edges_node)

    from_node = split_edges_node
    to_node = scale_elements_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

    from_node = scale_elements_node
    to_node = out_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])


def create_centerpiece():
    bpy.ops.mesh.primitive_plane_add()

    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]

    update_geo_node_tree(node_tree)

    bpy.ops.object.modifier_add(type="SOLIDIFY")


def main():
    """
    Python code to generate an animated geo nodes node tree
    that consists of a subdivided & triangulated cube with animated faces
    """
    scene_setup()
    create_centerpiece()


if __name__ == "__main__":
    main()



'''
#export
blend_file_path = file_path
directory = os.path.dirname(blend_file_path)
export_file_path = os.path.join(directory, "Strap_New") 
bpy.ops.export_scene.gltf(filepath=export_file_path, use_selection=True)
'''