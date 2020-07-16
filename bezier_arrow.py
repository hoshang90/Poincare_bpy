import bpy
import bmesh

#Size parameters
body_length = 4
body_width = 0.6
head_length = 1.1
head_width = 1

#Half sizes along Z
half_body_width = body_width / 2.0
half_head_width = head_width / 2.0

#Define the wanted coordinates
coords = [ [body_length, 0.0, half_body_width],       #1
            [body_length, 0.0, half_head_width],      #2
            [body_length + head_length, 0.0, 0.0],    #3
            [body_length, 0.0, -half_head_width],     #4
            [body_length, 0.0, -half_body_width],     #5
            [-body_length, 0.0, -half_body_width],    #6
            [-body_length, 0.0, -half_head_width],    #7
            [-body_length - head_length, 0.0, 0.0],   #8
            [-body_length, 0.0, half_head_width],     #9
            [-body_length, 0.0, half_body_width] ]    #10

#Create the mesh
bpy.ops.object.add(type='MESH')
#Get the object
obj = bpy.context.object
#Get the mesh data
mesh = obj.data

#Create a bmesh instance in order to add data (vertices and faces) to the mesh
bm = bmesh.new()

#Create the vertices
for coord in coords:
    bm.verts.new(coord)

#Add a face with all the vertices (the vertices order matters here)
bm.faces.new(bm.verts)

#Updates to Blender
bm.to_mesh(mesh)
mesh.update()