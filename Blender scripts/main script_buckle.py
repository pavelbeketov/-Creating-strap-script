import bpy
import math
import sys
import os
import numpy

#upd position points
'''
max_middle_poin = (-0.049776, -1.3417, 6.7215)
min_middle_poin = (-0.049775, -3.5286, 2.9707)
'''






#thickness
thickness = sys.argv[7]
th = float(thickness)

'''
#choose X lenght
#leng  = sys.argv[8]
#len = float(leng)

#choose Y lenght
#soly = sys.argv[7]
#sol = float(soly)
'''
#choose number of count 
number = sys.argv[6]
count = int(number)


#set number of count
bpy.data.node_groups["Geometry Nodes.001"].nodes["Resample Curve"].inputs[2].default_value = count

#sol
#bpy.context.object.modifiers["GeometryNodes"]["Socket_3"][1] = sol

#len
#bpy.context.object.modifiers["GeometryNodes"]["Socket_3"][0] = len


#if need run script in Blender
#bpy.ops.import_scene.gltf(filepath="C:\\Python\\test\\test_p_3.glb")

#choose file
file_path = sys.argv[5]
bpy.ops.import_scene.gltf(filepath=file_path)

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
#_____________________

'''
# Получаем коллекцию объектов
objects = bpy.data.objects

# Получаем количество объектов в коллекции
num_objects = len(objects)

# Если в коллекции есть хотя бы два объекта
if num_objects >= 2:
    # Сбрасываем выделение для всех объектов
    bpy.ops.object.select_all(action='DESELECT')
    
    # Выбираем последний и предпоследний объекты
    for obj in objects[-2:]:
        obj.select_set(True)
else:
    print("Коллекция объектов пуста или содержит меньше двух объектов.")
'''

#for obj in objects[-1:-3:1]:
 #   obj.select_set(True)



for obj in objects:
    obj.select_set(True)

# Name object
obj_name = "Back"
obj_name1 = "Curve"
# Select False
bpy.data.objects[obj_name].select_set(False)
bpy.data.objects[obj_name1].select_set(False)


bpy.context.view_layer.objects.active = parent_object
bpy.ops.object.join()

#set pivot point and position 3d model
bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')
bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')

object_to_rotate = bpy.context.active_object 

#rotate model 
object_to_rotate.rotation_euler[0] += math.radians(90)

#resize
bpy.ops.transform.resize(value=(0.006, 0.006, 0.006))

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

objects = bpy.context.scene.objects

#remove extra triangle
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.tris_convert_to_quads()
bpy.ops.object.editmode_toggle()


#solidify
bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = th
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



#export
blend_file_path = file_path
directory = os.path.dirname(blend_file_path)
export_file_path = os.path.join(directory, "Strap_New") 
bpy.ops.export_scene.gltf(filepath=export_file_path, use_selection=True)
