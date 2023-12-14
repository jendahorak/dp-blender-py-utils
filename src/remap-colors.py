import bpy
import colorsys
import math
import bmesh


def hex_color_to_rgba(hex_color):
    """
    Converts a hexadecimal color code to RGBA format.

    Args:
        hex_color (str): The hexadecimal color code (e.g., "#FF0000").

    Returns:
        tuple: A tuple containing the RGBA values as floats between 0.0 and 1.0.

    Raises:
        None

    Example:
        >>> hex_color_to_rgba("#FF0000")
        (1.0, 0.0, 0.0, 1.0)
    """

    # remove the leading '#' symbol
    hex_color = hex_color[1:]

    # extracting the Red color component - RRxxxx
    red = int(hex_color[:2], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_red = red / 255
    linear_red = convert_srgb_to_linear_rgb(srgb_red)

    # extracting the Green color component - xxGGxx
    green = int(hex_color[2:4], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_green = green / 255
    linear_green = convert_srgb_to_linear_rgb(srgb_green)

    # extracting the Blue color component - xxxxBB
    blue = int(hex_color[4:6], 16)
    # dividing by 255 to get a number between 0.0 and 1.0
    srgb_blue = blue / 255
    linear_blue = convert_srgb_to_linear_rgb(srgb_blue)

    return tuple([linear_red, linear_green, linear_blue, 1.0])


def convert_srgb_to_linear_rgb(srgb_color_component: float) -> float:
    """
    Converting from sRGB to Linear RGB
    based on https://en.wikipedia.org/wiki/SRGB#From_sRGB_to_CIE_XYZ
    """
    if srgb_color_component <= 0.04045:
        linear_color_component = srgb_color_component / 12.92
    else:
        linear_color_component = math.pow(
            (srgb_color_component + 0.055) / 1.055, 2.4)

    return linear_color_component


def get_base_color(material_name, lookup_key):
    """
    Mapping function, mapping names of materials to hex values. 
    These have to be changed based on chosen color pallete. Works only discrete color palletes.
    """
    material_name = material_name.split('.')[0]

    lookupMap = {
        'sk': {
            'sedlova': '#66c2a5',
            'mansardova': '#fc8d62',
            'plocha': '#8da0cb',
            'pultova': '#e78ac3',
            'stanova': '#a6d854',
            'valbova': '#ffd92f',
            'jina': '#e5c494'
        },
        'co': {
            'komin': '#FC8D62',
            'vez': '#A6D854',
            'stresni_nastavba': '#8DA0CB',
            'vytahy_klimatizace': '#E78AC3',
            'hlavni_cast_objektu': '#E1E1E1',
        },
        'pk': {
            'svisla_stena': '#FFFFFF',
            'vodorovna_strecha': '#B2B2B2',
            'sikma_strecha': '#DE6034',
            'zakladova_deska': '#FFFFFF',
        },
        't': {
            'CityEngineTerrainMaterial': '#DDDDDD'
        }

    }

    # TODO - extend for plocha_kod a cast objektu
    # Default to white if not found
    lookup = lookupMap.get(lookup_key, {})
    return hex_color_to_rgba(lookup.get(material_name, '#ffffff'))


def create_new_mat_copy(old_mat_name, lookup_key):
    """
    Create a new material copy based on the given old material name.

    Parameters:
    old_mat_name (str): The name of the old material.

    Returns:
    bpy.types.Material: The newly created material copy.
    """
    newMat = bpy.data.materials.new(f'{old_mat_name}_copy')

    print('creating new mat color from old mat name:', old_mat_name)

    # newMat.use_nodes = True
    newMat.diffuse_color = get_base_color(old_mat_name, lookup_key)
    newMat.roughness = 1.0
    print()
    print('New Material Created')

    return newMat


def iterate_materials():
    """
    Iterates through the material slots of the 'buildings' object and creates a copy of each material
    that does not end with '_copy'.

    Returns:
        None
    """
    buildings_obj = bpy.data.objects.get(
        "buildings")  # Use get to handle potential None
    if buildings_obj is None:
        print("Object 'buildings' not found")
        return

    buildings_obj_active = bpy.context.active_object

    # Ensure the correct object is active
    bpy.context.view_layer.objects.active = buildings_obj_active
    bpy.ops.object.mode_set(mode='OBJECT')

    for material_slot in buildings_obj_active.material_slots:
        if material_slot.material:
            curr_mat = material_slot.material
            print('------------------ Inspecting Materials ------------------')
            print("    - Material Name:", material_slot.material.name)
            print(f'{curr_mat.name}')
            print(f'{material_slot.slot_index}')
            if not curr_mat.name.endswith("_copy"):
                newMat = create_new_mat_copy(curr_mat.name)
                # append new material
                buildings_obj_active.data.materials.append(newMat)
                print('New material appended.')
            else:
                print('Done copying mats')
    print('Done copying')


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


def iterate_selected_objects(lookup_key):
    """
    Iterates through the selected objects and creates a copy of each material
    that does not end with '_copy'. The old material is then deleted.

    Returns:
        None
    """
    for obj in bpy.context.selected_objects:
        if obj.data.materials:
            # Assume each object has one material
            curr_mat = obj.data.materials[0]
            print('------------------ Inspecting Materials ------------------')
            print("    - Material Name:", curr_mat.name)

            newMat = create_new_mat_copy(curr_mat.name, lookup_key)
            # Replace old material with new one
            obj.data.materials[0] = newMat
            old_mat_name = curr_mat.name  # Save old material name
            bpy.data.materials.remove(curr_mat)

            # if old_mat_name.startswith('CityEngineTerrainMaterial'):
            #     old_mat_name = 'terrain_ce'

            newMat.name = old_mat_name  # Rename new material
            print('New material replaced.')

    print('Done copying')


def merge_verts_by_distance(merge_threshold):
    """
    Merges vertices that are closer than the given merge threshold.

    Args:
        merge_threshold (float): The merge threshold in Blender units.

    Returns:
        None
    """
    for obj in bpy.context.selected_objects:
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles(threshold=merge_threshold)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')


# iterate_materials()
remove_empty()
iterate_selected_objects('sk')
merge_verts_by_distance(0.0001)
