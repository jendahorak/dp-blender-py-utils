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


def get_base_color(material_name):
    """
    Mapping function, mapping names of materials to hex values. 
    These have to be changed based on chosen color pallete. Works only discrete color palletes.
    """
    colorDict = {
        'sedlova': '#66c2a5',
        'mansardova': '#fc8d62',
        'plocha': '#8da0cb',
        'pultova': '#e78ac3',
        'stanova': '#a6d854',
        'valbova': '#ffd92f',
        'jina': '#e5c494',
    }

    # Default to white if not found
    return hex_color_to_rgba(colorDict.get(material_name, '#ffffff'))


def create_new_mat_copy(old_mat_name):
    """
    Create a new material copy based on the given old material name.

    Parameters:
    old_mat_name (str): The name of the old material.

    Returns:
    bpy.types.Material: The newly created material copy.
    """
    newMat = bpy.data.materials.new(f'{old_mat_name}_copy')

    print('creating new mat color from old mat name:',old_mat_name )

    # newMat.use_nodes = True
    newMat.diffuse_color = get_base_color(old_mat_name)
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
    buildings_obj = bpy.data.objects.get("buildings")  # Use get to handle potential None
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

iterate_materials()
# reassign_materials()