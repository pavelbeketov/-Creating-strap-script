import bpy
import math
import sys
import os

#choose file
file_path = sys.argv[5]
bpy.ops.import_scene.gltf(filepath=file_path)

#rename file 
object_to_rename = bpy.context.active_object
object_to_rename.name = "Strap"

#delete coordinate
object_to_delete = bpy.data.objects.get("Plane")

bpy.data.objects.remove(object_to_delete, do_unlink=True)

#choose object in Geometry Nodes
bpy.data.node_groups["Geometry Nodes.001"].nodes["Object Info"].inputs[0].default_value = bpy.data.objects["Strap"]


bpy.ops.object.select_all(action='SELECT')


#convert all scene in Mesh (bezie to mesh)
bpy.ops.object.convert(target='MESH')

#delete Plane befor export
object_name = "Strap" 
object_to_delete = bpy.data.objects.get(object_name)

bpy.data.objects.remove(object_to_delete, do_unlink=True)

#export
blend_file_path = file_path
directory = os.path.dirname(blend_file_path)
export_file_path = os.path.join(directory, "Strap_New") 
bpy.ops.export_scene.gltf(filepath=export_file_path, use_selection=True)