import bpy

vertices = [
    (0.0, 0.0, 0.0),  # 0
    (1.0, 0.0, 0.0),  # 1
    (0.0, 1.0, 0.0),  # 2
    (0.0, 0.0, 1.0),  # 3
    (1.0, 1.0, 1.0),  # 4
    (1.0, 1.0, 0.0),  # 5
    (1.0, 0.0, 1.0),  # 6
    (0.0, 1.0, 1.0),  # 7
]

faces = [
    (0, 1, 6, 3),  # Frontface
    (2, 7, 4, 5),  # Backface
    (0, 3, 7, 2),  # Leftface
    (1, 5, 4, 6),  # Rightface
    (0, 2, 5, 1),  # Bottomface
    (3, 6, 4, 7),  # Topface
]

vertices_two = [
    (0.0, 0.0, 1.0),  # 0 (3)
    (1.0, 1.0, 1.0),  # 1 (4)
    (1.0, 0.0, 1.0),  # 2 (6)
    (0.0, 1.0, 1.0),  # 3 (7)
]

faces_two = [(0, 2, 1, 3)]


mesh_data = bpy.data.meshes.new("test_cube_half")
mesh_data.from_pydata(vertices, [], faces[:-1])

obj = bpy.data.objects.new("Half_Cube", mesh_data)
mat = bpy.data.materials.new(name="Test_Material_one")
obj.data.materials.append(mat)
bpy.context.collection.objects.link(obj)


mesh_data_two = bpy.data.meshes.new("Test_top_face")
mesh_data_two.from_pydata(vertices_two, [], faces_two)

obj_two = bpy.data.objects.new("My_object_two", mesh_data_two)
mat_two = bpy.data.materials.new(name="Test_Material_two")
obj_two.data.materials.append(mat_two)

bpy.context.collection.objects.link(obj_two)

bpy.ops.object.select_all(action='SELECT')

bpy.ops.object.join()

#objectToSelect = bpy.data.objects["objectName"]
#objectToSelect.select_set(True)    
#bpy.context.view_layer.objects.active = objectToSelect
#bpy.ops.object.select_all(action='DESELECT')

# to rename data of an object 
# aa=bpy.context.object.data
#aa.name='bb'
### but to rename the object 
#>>> aa=bpy.context.object
#>>> aa.name='bb'

## to select objects 
#>>> objectToSelect = bpy.data.objects["bb"]
#>>> objectToSelect.select_set(True)