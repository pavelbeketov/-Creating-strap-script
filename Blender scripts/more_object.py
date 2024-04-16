import bpy
import math
import sys
import os
import numpy

'''
max_middle_poin = (-0.049776, -1.1891, 4.5373)
min_middle_poin = (-0.049775, -3.3185, 1.0538)
'''
#choose Y lenght
soly = sys.argv[7]
sol = float(soly)

#choose number of count 
number = sys.argv[6]
count = int(number)


#set number of count
bpy.data.node_groups["Geometry Nodes.001"].nodes["Resample Curve"].inputs[2].default_value = count

#bpy.data.node_groups["Geometry Nodes.001"].nodes["Instance on Points"].inputs[6].default_value[1] = sol
bpy.context.object.modifiers["GeometryNodes"]["Socket_3"][1] = sol

#if need run script in Blender
#bpy.ops.import_scene.gltf(filepath="C:\\path to file\\")


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
bpy.ops.object.transform_apply()

objects = bpy.context.scene.objects


#solidify
bpy.ops.object.modifier_add(type='SOLIDIFY')
bpy.context.object.modifiers["Solidify"].thickness = 0.1
bpy.ops.object.modifier_apply(modifier="Solidify")


#bevel
bpy.ops.object.modifier_add(type='BEVEL')
bpy.context.object.modifiers["Bevel"].segments = 5
bpy.ops.object.modifier_apply(modifier="Bevel")


#choose object in Geometry Nodes
bpy.data.node_groups["Geometry Nodes.001"].nodes["Object Info"].inputs[0].default_value = bpy.data.objects["Plane"]

bpy.ops.object.select_all(action='SELECT')

#convert all scene in Mesh (bezie -> mesh)
bpy.ops.object.convert(target='MESH')


#delete Plane befor export
object_name = "Plane" 
object_to_delete = bpy.data.objects.get(object_name)

bpy.data.objects.remove(object_to_delete, do_unlink=True)


#star adding atribute point
'''
obj = bpy.data.objects["Curve"]

# Установите объект как активный
bpy.context.view_layer.objects.active = obj


bpy.ops.object.editmode_toggle()


#create max middle point
bpy.ops.mesh.primitive_vert_add()
bpy.ops.transform.translate(value=(max_middle_poin))

#create min middle point
bpy.ops.mesh.primitive_vert_add()
bpy.ops.transform.translate(value=(min_middle_poin))

bpy.ops.object.editmode_toggle()

#bpy.ops.geometry.attribute_add(name="gfd", data_type='INT')

mesh = bpy.context.collection.objects["Curve"].data
attribute = mesh.attributes.new(name="new attribute", type="INT", domain="POINT")


# Получите количество вершин в сетке
num_vertices = len(mesh.vertices)

# Создайте список атрибутов
attribute_values = [0] * num_vertices

# Установите последние два значения атрибута на 1
attribute_values[num_vertices - 2:] = [1, 1]

# Обновите атрибут данными
attribute.data.foreach_set("value", attribute_values)

bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
'''

#export
blend_file_path = file_path
directory = os.path.dirname(blend_file_path)
export_file_path = os.path.join(directory, "Strap_New") 
bpy.ops.export_scene.gltf(filepath=export_file_path, use_selection=True)