import bpy
import bmesh

#Define the wanted coordinates
coords = [ [1, 0.0, 1] ]    #10
#Create the mesh
bpy.ops.object.add(type='MESH')
#Get the object
obj = bpy.context.object
#Get the mesh data
mesh = obj.data
#Create a bmesh instance in order to add data (vertices and faces) to the mesh
bm = bmesh.new()
#Create the vertices
#for coord in coords:
bm.verts.new(coords[0])
#Add a face with all the vertices (the vertices order matters here)
#bm.faces.new(bm.verts)
#Updates to Blender
bm.to_mesh(mesh)
mesh.update()
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
#change it to bezier curve and make it 3d
#bpy.ops.object.convert(target='CURVE')
#obj = bpy.context.object
#obj.data.dimensions = '3D'
#obj.data.fill_mode = 'FULL'
#radius of the curve
#obj.data.bevel_depth =0.11
#obj.data.bevel_resolution = 20 #resolution of the object
