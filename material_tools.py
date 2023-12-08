import bpy

def remove_all_materials():
    """
    Remove all materials from the current Blender file.
    """
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)

def remove_all_meshes():
    """
    Remove all meshes from the current Blender file.
    """
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)


remove_all_materials()
remove_all_meshes()