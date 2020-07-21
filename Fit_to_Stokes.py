import bpy
import sys
import bmesh
import numpy as np
from scipy import optimize 
# to install package in python blender we need to go to python console
# import sys;sys.exec_prefix  ---> which will give the python postion then run powershell as addministroto and 
# cd to the output
# then run .\bin\python.exe -m ensurepip; then .\bin\python.exe -m pip install --upgrade pip
# then run .\bin\python.exe -m pip install module name such as scipy 

data=np.loadtxt("C:\\Users\\Home\\Google Drive\\blender\\blender_python\\Stokes")#for windows
#data=np.loadtxt("/home/hoshang/Stamp_sample_guiding/blender/Stokes")#for linux

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
def line_between(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2, r=Line_radius):
    bpy.ops.curve.primitive_bezier_curve_add()
    obj = bpy.context.object
    obj.data.dimensions = '3D'
    obj.data.fill_mode = 'FULL'
    obj.data.bevel_depth = Line_radius
    obj.data.bevel_resolution = 20
    # set first point to centre of sphere1
    obj.data.splines[0].bezier_points[0].co = (x1,y1,z1)
    obj.data.splines[0].bezier_points[0].handle_left_type = 'VECTOR'
    # set second point to centre of sphere2
    obj.data.splines[0].bezier_points[1].co = (x2,y2,z2)
    obj.data.splines[0].bezier_points[1].handle_left_type = 'VECTOR'

def cylinder_between(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2,\
        r=Cylinder_radius,r_cone=Cone_radius,d_cone=Cone_depth,\
        color='red',Rot_axis_x=0,Rot_axis_y=0,Rot_axis_z=0\
        ,x_angle=0,y_angle=0,z_angle=0,Rot_reset=0,Name="Eigenmode_arrow"):
    arrow_mat=bpy.data.materials.new("arrow_material")#create the material and point to it
    if color=='red':
        arrow_mat.diffuse_color = (1, 0, 0, 1)#make the materials red
    elif color=='green':
        arrow_mat.diffuse_color = (0, 1, 0, 1)
    elif color=='blue':
        arrow_mat.diffuse_color = (0, 0, 1, 1)
    elif color=='white':
        arrow_mat.diffuse_color = (1, 1, 1, 1)
    elif color=='black':
        arrow_mat.diffuse_color = (0, 0, 0, 1)
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = np.sqrt(dx**2 + dy**2 + dz**2)
    bpy.ops.mesh.primitive_cylinder_add(enter_editmode=True,
        radius = r, 
        depth = dist,
        location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)) 
    bpy.ops.mesh.primitive_cone_add(radius1=Cone_radius, depth=d_cone,\
            enter_editmode=False, location=(dx/2 + x1, dy/2 + y1, dz/2 + z1))
    bpy.ops.transform.translate(value=(0, 0, dist/2), orient_type='GLOBAL')
    bpy.ops.mesh.primitive_cone_add(radius1=Cone_radius, depth=d_cone,\
            enter_editmode=False, location=(dx/2 + x1, dy/2 + y1, dz/2 + z1))
    bpy.ops.transform.rotate(value=np.pi, orient_axis='X', orient_type='GLOBAL')
    bpy.ops.transform.translate(value=(0, 0, -dist/2), orient_type='GLOBAL')
    phi = np.arctan2(dy, dx) 
    theta = np.arccos(dz/dist) 
    bpy.ops.object.editmode_toggle()
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')    
    mesh = bpy.context.object.data
    mesh.materials.clear()#clear other materials linked to the objects
    mesh.materials.append(arrow_mat)
    bpy.context.object.rotation_euler[1] = theta 
    bpy.context.object.rotation_euler[2] = phi
    if Rot_reset==1:
        bpy.ops.object.rotation_clear()
    if Rot_axis_x==1:
        bpy.context.object.rotation_euler[0] = x_angle
    elif Rot_axis_y==1:
        bpy.context.object.rotation_euler[1] = y_angle
    elif Rot_axis_z==1:
        bpy.context.object.rotation_euler[2] = z_angle
    bpy.context.object.name=Name

def rotate_with_cursor(x1=x1, y1=y1, z1=z1, x2=x2, y2=y2, z2=z2,psi=psi_rad,data=data,calculated_sphere_radius=0.02,input_torus_radius=0.01, calc_torus_radius=0.01):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = np.sqrt(dx**2 + dy**2 + dz**2)
    phi = np.arctan2(dy, dx) 
    theta = np.arccos(dz/dist)
    bpy.context.scene.cursor.rotation_euler[1] = theta
    bpy.context.scene.cursor.rotation_euler[2] = phi
    
    calc_torus_mat=bpy.data.materials.new("calculated_polarization")#create the input material and point to it
    calc_torus_mat.diffuse_color = (1, 1, 1, 1)#make the materials blue
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), rotation=(0, 0, 0), major_radius=1, minor_radius=calc_torus_radius, abso_major_rad=1.25, abso_minor_rad=0.75)
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    bpy.ops.transform.rotate(value=np.pi/2, orient_axis='X')
    bpy.ops.transform.rotate(value=psi, orient_axis='Z', orient_type='CURSOR')
    mesh = bpy.context.object.data
    mesh.materials.clear()#clear other materials linked to the objects
    mesh.materials.append(calc_torus_mat)
    bpy.context.object.name="Output_torus"
    calc_mat=bpy.data.materials.new("calculated_polarization")#create the input material and point to it
    calc_mat.diffuse_color = (0, 0, 0, 1)#make the materials blue
    for i in range(len(data[:,0])):
        ##### create calculated polarizations with small spheres
        bpy.ops.mesh.primitive_uv_sphere_add(radius=calculated_sphere_radius,location=(data[i,0], data[i,1], data[i,2]),segments=20, ring_count=20)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')#change origin of the spheres otherwise they will not rotate        
        bpy.ops.transform.rotate(value=psi, orient_axis='Z', orient_type='CURSOR')
        mesh = bpy.context.object.data
        mesh.materials.clear()#clear other materials linked to the objects
        mesh.materials.append(calc_mat)
        bpy.context.object.name="Calc_spheres"+str(i)
    for i in range(len(data[:,0])):
        bpy.data.objects["Calc_spheres"+str(i)].select_set(True)
    bpy.ops.object.join()
    bpy.context.object.name="cal_spheres"    

def make_input_ouput_sphere(data=data,input_radius=0.03,output_radius=0.03,psi=psi_rad, calc_torus_radius=0.01):
    mat_input=bpy.data.materials.new("input_polarization")#create the input material and point to it
    mat_input.diffuse_color = (0, 0.00333301, 0.8, 1)#make the materials blue
    ###
    mat_output=bpy.data.materials.new("output_polarization")#create the output material and point to it
    mat_output.diffuse_color = (0.00156367, 0.447979, 0.0282846, 1)#make the materials green
    
    mat_torus_input=bpy.data.materials.new("input_torus")#create the output material and point to it
    mat_torus_input.diffuse_color = (1, 1, 1, 1)#make the materials white
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), rotation=(0, 0, 0), major_radius=1, minor_radius=calc_torus_radius, abso_major_rad=1.25, abso_minor_rad=0.75)
    bpy.ops.transform.rotate(value=np.pi/2, orient_axis='X')
    mesh = bpy.context.object.data
    mesh.materials.clear()#clear other materials linked to the objects
    mesh.materials.append(mat_torus_input)
    bpy.context.object.name="Input_torus"
    #bpy.ops.mesh.primitive_uv_sphere_add(radius=1,segments=100, ring_count=100,location=(0, 0, 0))
    for i in range(len(data[:,0])):
        ##### create input polarizations with small spheres
        bpy.ops.mesh.primitive_uv_sphere_add(radius=input_radius,location=(data[i,0], data[i,1], data[i,2]),segments=20, ring_count=20)
        mesh = bpy.context.object.data
        mesh.materials.clear()#clear other materials linked to the objects
        mesh.materials.append(mat_input)
        bpy.context.object.name="Input_sphere"+str(i)
        ###### create output polarization with small spheres
        bpy.ops.mesh.primitive_uv_sphere_add(radius=output_radius,location=(data[i,4], data[i,5], data[i,6]),segments=20, ring_count=20)
        mesh = bpy.context.object.data
        mesh.materials.clear()
        mesh.materials.append(mat_output)  
        bpy.context.object.name="Output_sphere"+str(i) 
    bpy.ops.object.select_all(action='DESELECT')
    for i in range(len(data[:,0])):
        bpy.data.objects["Input_sphere"+str(i)].select_set(True)
        bpy.data.objects["Output_sphere"+str(i)].select_set(True)
    bpy.ops.object.join()
    bpy.context.object.name="Input_Out_spheres"
def make_earth_sphere(sphere_r=2,arrows_r=0.01): 
    mat = bpy.data.materials.new("earth")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load("C:\\Users\\Home\\Google Drive\\blender\\blender_python\\2k_earth_daymap.jpg")
    #texImage.image = bpy.data.images.load("/home/hoshang/Stamp_sample_guiding/blender/2k_earth_daymap.jpg")
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1,location=(0,0,0),segments=50, ring_count=50)
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 4
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    mesh = bpy.context.object.data
    mesh.materials.clear()
    mesh.materials.append(mat)
    bpy.context.object.name="Earth_sphere"
def make_3d_poincare():
    Cone_radius=0.03;Cone_depth=0.04;p=np.pi
    cylinder_between(x1=1.5, y1=0, z1=0, x2=-1.5, y2=0, z2=0,r=Cylinder_radius\
            ,r_cone=Cone_radius,d_cone=Cone_depth,color='black',Name="S1_axis")#X_axis S1
    cylinder_between(x1=1.3, y1=0, z1=0, x2=1.5, y2=0,z2=0,r=Cylinder_radius\
                    ,r_cone=Cone_radius,d_cone=Cone_depth,color='red',Rot_reset=1,Rot_axis_x=1,x_angle=p/2,Name="TE")#s1=1TE
    cylinder_between(x1=-1.3, y1=0, z1=0, x2=-1.5, y2=0,z2=0,r=Cylinder_radius\
                    ,r_cone=Cone_radius,d_cone=Cone_depth,color='blue',Rot_reset=1,Name="TM")#s1=-1TM
    cylinder_between(x1=0, y1=1.5, z1=0, x2=0, y2=-1.5, z2=0,r=Cylinder_radius\
            ,r_cone=Cone_radius,d_cone=Cone_depth,color='black',Name="S2_axis")#Y_axis S2
    cylinder_between(x1=0, y1=1.3, z1=0, x2=0, y2=1.5,z2=0,r=Cylinder_radius\
                    ,r_cone=Cone_radius,d_cone=Cone_depth,color='red',Rot_reset=1,Rot_axis_y=1,y_angle=-p/4,Name="S2+45")#S2=1>+45
    cylinder_between(x1=0, y1=-1.3, z1=0, x2=0, y2=-1.5,z2=0,r=Cylinder_radius\
                    ,r_cone=Cone_radius,d_cone=Cone_depth,color='blue',Rot_reset=1,Rot_axis_y=1,y_angle=p/4,Name="S2-45")#S2=-1>-45
    cylinder_between(x1=0, y1=0, z1=1.5, x2=0, y2=0, z2=-1.5,r=Cylinder_radius\
            ,r_cone=Cone_radius,d_cone=Cone_depth,color='black',Name="S3_axis")#Z_axis S3
def make_RHP_LHP(x=0,y=0,z=0,R_major=0.2,R_minor=0.01,Handness='right'):
    mat_red=bpy.data.materials.new("mat_red")
    mat_red.diffuse_color = (1, 0, 0, 1)
    mat_blue=bpy.data.materials.new("mat_blue")
    mat_blue.diffuse_color = (0, 0, 1, 1)
    bpy.ops.mesh.primitive_torus_add(location=(x, y, z), rotation=(0, 0, 0),
            major_radius=R_major, minor_radius=R_minor)
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = 3
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")
    bpy.ops.object.editmode_toggle()
    if Handness=='right':
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0, depth=0.06, enter_editmode=False, \
        align='WORLD', location=(-R_major, 0, 0), rotation=(-np.pi/2, 0, 0))
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0, depth=0.06, enter_editmode=False, \
        align='WORLD', location=(R_major, 0, 0), rotation=(np.pi/2, 0, 0))
        bpy.ops.object.editmode_toggle()
        mesh = bpy.context.object.data
        mesh.materials.clear()#clear other materials linked to the objects
        mesh.materials.append(mat_red)
        bpy.context.object.location[2] = 1.4
        bpy.context.object.name="RHC_polarization"
    elif Handness=='left':
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0, depth=0.06, enter_editmode=False, \
        align='WORLD', location=(R_major, 0, 0), rotation=(-np.pi/2, 0, 0))
        bpy.ops.mesh.primitive_cone_add(radius1=0.03, radius2=0, depth=0.06, enter_editmode=False, \
        align='WORLD', location=(-R_major, 0, 0), rotation=(np.pi/2, 0, 0))
        bpy.ops.object.editmode_toggle()
        mesh = bpy.context.object.data
        mesh.materials.clear()#clear other materials linked to the objects
        mesh.materials.append(mat_blue)
        bpy.context.object.location[2] = -1.4
        bpy.context.object.name="LHC_polarization"

def Make_curves(x1=x1, y1=y1, z1=z1, x2=x2,y2=y2,z2=z2,psi=psi_rad,data=data,curve_radius=0.01):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = np.sqrt(dx**2 + dy**2 + dz**2)
    phi = np.arctan2(dy, dx) 
    theta = np.arccos(dz/dist)
    bpy.context.scene.cursor.rotation_euler[1] = theta
    bpy.context.scene.cursor.rotation_euler[2] = phi
    curves_mat=bpy.data.materials.new("curve_material")
    curves_mat.diffuse_color = (1, 1, 1, 1)#white   
    for i in range(len(data[:,0])):
        for j in np.arange(0,psi,psi/30):
            #Create the mesh
            bpy.ops.object.add(type='MESH')
            #Get the object
            obj = bpy.context.object
            #Get the mesh data
            mesh = obj.data
            #Create a bmesh instance in order to add data (vertices and faces) to the mesh
            bm = bmesh.new()
            #Create the vertices
            #[x,y,z]
            bm.verts.new([data[i,0],data[i,1],data[i,2]])
            #Add a face with all the vertices (the vertices order matters here)
            #bm.faces.new(bm.verts)
            #Updates to Blender
            bm.to_mesh(mesh)
            mesh.update()
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.transform.rotate(value=j, orient_axis='Z', orient_type='CURSOR')
            bpy.context.object.name=str(i+j)
        for j in np.arange(0,psi,psi/30):
            bpy.data.objects[str(i+j)].select_set(True)
        bpy.ops.object.join()
        bpy.context.object.name="input_cal_curve"+str(i)
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()
        #change it to bezier curve and make it 3d
        bpy.ops.object.convert(target='CURVE')
        obj = bpy.context.object
        obj.data.dimensions = '3D'
        obj.data.fill_mode = 'FULL'
        obj.data.bevel_depth =curve_radius
        obj.data.bevel_resolution = 20 #resolution of the object
        mesh = bpy.context.object.data
        mesh.materials.clear()
        mesh.materials.append(curves_mat)

def Make_curves_withObj(x1=x1, y1=y1, z1=z1, x2=x2,y2=y2,z2=z2,psi=psi_rad,data=data,curve_radius=0.01,obj_num=50, cone_arrow=False):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1    
    dist = np.sqrt(dx**2 + dy**2 + dz**2)
    phi = np.arctan2(dy, dx) 
    theta = np.arccos(dz/dist)
    bpy.context.scene.cursor.rotation_euler[1] = theta
    bpy.context.scene.cursor.rotation_euler[2] = phi
    curves_mat=bpy.data.materials.new("curve_material")
    curves_mat.diffuse_color = (0, 1, 1, 1)#white   
    for i in range(len(data[:,0])):
        for j in np.arange(0,psi,psi/obj_num):
            bpy.ops.mesh.primitive_cube_add(size=curve_radius, location=(data[i,0],data[i,1],data[i,2]))
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.transform.rotate(value=j, orient_axis='Z', orient_type='CURSOR')
            bpy.context.object.name=str(i+j)
            if cone_arrow==True and j==psi/(obj_num/2):
                bpy.ops.mesh.primitive_cone_add(radius1=curve_radius*3, depth=curve_radius*4, location=(data[i,0],data[i,1],data[i,2]))
                if data[i,0] >0:
                    bpy.ops.transform.rotate(value=-np.pi/2, orient_axis='X', orient_type='GLOBAL')
                else:
                    bpy.ops.transform.rotate(value=np.pi/2, orient_axis='X', orient_type='GLOBAL')
                bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
                bpy.ops.transform.rotate(value=psi/2, orient_axis='Z', orient_type='CURSOR')
                bpy.context.object.name="cone"+str(i)
        for j in np.arange(0,psi,psi/obj_num):
            bpy.data.objects[str(i+j)].select_set(True)
            if cone_arrow==True and j==psi/(obj_num/2):
                bpy.data.objects["cone"+str(i)].select_set(True)
        bpy.ops.object.join()
        bpy.context.object.name="input_cal_curve"+str(i)
        mesh = bpy.context.object.data
        mesh.materials.clear()
        mesh.materials.append(curves_mat)
        bpy.ops.object.select_all(action='DESELECT')
    for i in range(len(data[:,0])):
        bpy.data.objects["input_cal_curve"+str(i)].select_set(True)
    bpy.ops.object.join()
    bpy.context.object.name="input_cal_curves"
    bpy.ops.object.select_all(action='DESELECT')

def Rotate_around(number_of_frames=200):
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    bpy.context.object.name="Base_for_rotate"
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects["Camera"].select_set(True)
    bpy.data.objects["Base_for_rotate"].select_set(True)
    bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.frame_end = number_of_frames
    bpy.context.scene.frame_current = 1
    bpy.data.objects["Base_for_rotate"].select_set(True)
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.context.scene.frame_current = int(number_of_frames/1.7)
    bpy.ops.transform.rotate(value=np.pi, orient_axis='Z', orient_type='GLOBAL')
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.context.scene.frame_current =int(number_of_frames/1.3) 
    bpy.ops.transform.rotate(value=np.pi*1.5, orient_axis='Z', orient_type='GLOBAL')
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.context.scene.frame_current = number_of_frames
    bpy.ops.transform.rotate(value=np.pi*1.5, orient_axis='Z', orient_type='GLOBAL')
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
    bpy.ops.object.select_all(action='DESELECT')

rotate_with_cursor() # to rotate the cusor and rotate the torus 
cylinder_between() #to create a Cylinder between the eigen modes
#line_between() #to create a line between the eigen modes
make_input_ouput_sphere()
make_earth_sphere()
make_3d_poincare()
make_RHP_LHP(x=0,y=0,z=0,Handness='left')
make_RHP_LHP(x=0,y=0,z=0,Handness='right')
#Make_curves()
Make_curves_withObj(cone_arrow=False)
#Rotate_around()
