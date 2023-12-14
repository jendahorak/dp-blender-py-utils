import bpy
import bpy
import bmesh
from mathutils import Vector


def cleanup_geometry():
    bpy.ops.object.select_all(action='DESELECT')

    # Create a new mesh for joining all objects
    bpy.ops.object.select_by_type(type='MESH')
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active.name = "buildings"
    merge_threshold = 0.0001

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.remove_doubles(threshold=merge_threshold)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_mode(type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)


cleanup_geometry()
