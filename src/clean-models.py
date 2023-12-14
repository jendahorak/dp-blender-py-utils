import bpy

# def process_objects():
#     # Create a new mesh for joining all selected objects
#     bpy.ops.object.select_by_type(type='MESH')
#     bpy.context.view_layer.objects.active = bpy.context.selected_objects[0]
#     bpy.ops.object.join()
#     bpy.context.view_layer.objects.active.name = "buildings"


#     # Iterate through all materials in the selected objects
#     all_materials = set()
#     for obj in bpy.context.selected_objects:
#         if obj.type == 'MESH':
#             for material_slot in obj.material_slots:
#                 if material_slot.material:
#                     all_materials.add(material_slot.material)

#     # Assign materials to the new "buildings" mesh, checking for duplicates
#     buildings_obj = bpy.data.objects["buildings"]
#     for material in all_materials:
#         if material.name not in [mat.name for mat in buildings_obj.data.materials]:
#             buildings_obj.data.materials.append(material)
#     print()
#     print('Materials assigned to the new buildings mesh.')


def process_objects_terrain():
    # Create a new mesh for joining all selected objects
    bpy.ops.object.select_by_type(type='MESH')

    # Rename objects containing "terrain" in their name and exclude them from the "buildings" mesh
    terrain_objects = [
        obj for obj in bpy.context.selected_objects if 'terrain' in obj.name.lower()]
    for obj in terrain_objects:
        obj.name = "terrain"
        obj.select_set(False)

        # Rename the material of the "terrain" object
        for material_slot in obj.material_slots:
            material_slot.material.name = "terrain_ce"

    # Set the active object to the first selected object that is not a "terrain" object
    bpy.context.view_layer.objects.active = [
        obj for obj in bpy.context.selected_objects if obj not in terrain_objects][0]

    bpy.ops.object.join()
    bpy.context.view_layer.objects.active.name = "buildings"
    # Set the active object's data block name to match the object name
    bpy.context.view_layer.objects.active.data.name = "buildings_mesh"

    # Iterate through all materials in the selected objects
    all_materials = set()
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for material_slot in obj.material_slots:
                if material_slot.material:
                    all_materials.add(material_slot.material)

    # Assign materials to the new "buildings" mesh, checking for duplicates
    buildings_obj = bpy.data.objects["buildings"]
    for material in all_materials:
        if material.name not in [mat.name for mat in buildings_obj.data.materials]:
            buildings_obj.data.materials.append(material)
    print()
    print('Materials assigned to the new buildings mesh.')


def remove_empty():
    # Iterate through all selected objects in the scene
    for obj in bpy.context.selected_objects:
        print()
        print("Object Name:", obj.name)
        print("Object Type:", obj.type)
        print("Is Mesh:", obj.type == 'MESH')

        if obj.type == 'EMPTY':
            print(f'{obj.name} removed !!')
            bpy.data.objects.remove(obj, do_unlink=True)
            continue
    print('Removed all empty objects.')


remove_empty()
# process_objects()
# process_objects_terrain()
