import bpy


def remove_unused_materials():
    """
    Remove all unused materials from the current Blender file.
    """
    for material in bpy.data.materials:
        if material.users == 0:
            bpy.data.materials.remove(material)


def remove_unused_meshes():
    """
    Remove all unused meshes from the current Blender file.
    """
    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)


def delete_all_objects():
    """
    Select all objects in the scene and delete them.
    """
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)


# delete_all_objects()
remove_unused_materials()
remove_unused_meshes()
