import bpy
import numpy as np
#myObj.select = True
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
bpy.context.object.name="Base_for_rotate"
bpy.ops.object.select_all(action='DESELECT')
bpy.data.objects["Camera"].select_set(True)
bpy.data.objects["Base_for_rotate"].select_set(True)
bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
bpy.ops.object.select_all(action='DESELECT')
bpy.context.scene.frame_end = 200
bpy.context.scene.frame_current = 1
bpy.data.objects["Base_for_rotate"].select_set(True)
bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
bpy.context.scene.frame_current = 120
bpy.ops.transform.rotate(value=np.pi, orient_axis='Z', orient_type='GLOBAL')
bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
bpy.context.scene.frame_current = 150
bpy.ops.transform.rotate(value=np.pi*1.5, orient_axis='Z', orient_type='GLOBAL')
bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
bpy.context.scene.frame_current = 200
bpy.ops.transform.rotate(value=np.pi*1.5, orient_axis='Z', orient_type='GLOBAL')
bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')
