import bpy
import bmesh #for make_curves_function
import sys
import numpy as np
from scipy import optimize 
# to install package in python blender we need to go to python console
# import sys;sys.exec_prefix  ---> which will give the python postion then run powershell as addministroto and 
# cd to the output
# then run .\bin\python.exe -m ensurepip; then .\bin\python.exe -m pip install --upgrade pip
# then run .\bin\python.exe -m pip install module name such as scipy 

#data=np.loadtxt("C:\\Users\\Home\\Google Drive\\blender\\blender_python\\Stokes")#for windows
data=np.loadtxt("/home/hoshang/Stamp_sample_guiding/blender/Stokes")#for linux

# param=angle mode propre, angle rotation, angle tilt
def rot_diff(param,vstokes):
    """ 
    Stokes(tourné)-Stokes(Init)
    Stokes(tourné): rotation autours du mode propre de psi
    mode propre= u definit ci dessous
    """
    t0,psi,tilt = param
    # coordonnes ux,uy,uz du mode propre en fonction de teta et de tilt
    ux=np.cos(2*t0)*np.cos(2*tilt)
    uy=np.cos(2*t0)*np.sin(2*tilt)
    uz=np.sin(2*t0)
    # rotation de psi autour de u=(ux,uy,uz)
    S1=vstokes[:,0]*(ux*ux*(1-np.cos(psi))+np.cos(psi))
    S1+=vstokes[:,2]*(ux*uz*(1-np.cos(psi))+uy*np.sin(psi))

    S2=vstokes[:,0]*(ux*uy*(1-np.cos(psi))+uz*np.sin(psi))
    S2+=vstokes[:,2]*(uy*uz*(1-np.cos(psi))-ux*np.sin(psi))

    S3=vstokes[:,1]*(ux*uz*(1-np.cos(psi))-uy*np.sin(psi))
    S3+=vstokes[:,2]*(uz*uz*(1-np.cos(psi))+np.cos(psi))

    diff=np.column_stack((S1,S2,S3))-vstokes[0:,4:]
    #le ravel met a plat le tableau
    return(diff.ravel())
#print(data[:,4:])
#print(vrot)
x0=[np.deg2rad(45),np.deg2rad(-45),0]
sol,flag =optimize.leastsq(rot_diff,x0,args=(data))
#print(np.rad2deg(sol)[0],np.rad2deg(sol)[1],np.rad2deg(sol)[2])
rmp=1.5
Cylinder_radius=0.01
Cone_radius=0.03
Cone_depth=0.06
Line_radius=0.011
teta_rad=(sol)[0]
psi_rad=(sol)[1]
tilt_rad=(sol)[2]
x1,y1,z1=rmp*np.cos(2*teta_rad)*np.cos(2*tilt_rad),rmp*np.cos(2*teta_rad)*\
np.sin(2*tilt_rad),rmp*np.sin(2*teta_rad)
x2,y2,z2=-x1,-y1,-z1
#bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05,location=(rmp*-0.1252512741724018,rmp*-0.038713996591008645,rmp*0.29530603684894835),segments=20, ring_count=20)


def Make_curves(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = np.sqrt(dx**2 + dy**2 + dz**2)
    phi = np.arctan2(dy, dx) 
    theta = np.arccos(dz/dist)
    bpy.context.scene.cursor.rotation_euler[1] = theta
    bpy.context.scene.cursor.rotation_euler[2] = phi

    All_coords=data[:,0:2]
    
    #Half sizes along Z
    half_body_width = body_width / 2.0
    half_head_width = head_width / 2.0
    
    #Define the wanted coordinates
    coords = [ [body_length, 0.0, half_body_width],       #1

    #Create the mesh
    bpy.ops.object.add(type='MESH')
    #Get the object
    #obj = bpy.context.object
    #Get the mesh data
    mesh = obj.data
    
    #Create a bmesh instance in order to add data (vertices and faces) to the mesh
    bm = bmesh.new()
    
    #Create the vertices
    for coord in coords:
        bm.verts.new(coord)
    
    #Add a face with all the vertices (the vertices order matters here)
    #bm.faces.new(bm.verts)
    
    #Updates to Blender
    bm.to_mesh(mesh)
    mesh.update()
    ##change it to bezier curve and make it 3d
    #bpy.ops.object.convert(target='CURVE')
    #obj = bpy.context.object
    #obj.data.dimensions = '3D'
    #obj.data.fill_mode = 'FULL'
    ##radius of the curve
    #obj.data.bevel_depth =0.11
    #obj.data.bevel_resolution = 20 #resolution of the object
    
#Make_curves()
#bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL'})
#bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
#bpy.ops.transform.rotate(value=-0.390753, orient_axis='Z', orient_type='CURSOR')