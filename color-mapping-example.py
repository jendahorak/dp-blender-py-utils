# give Python access to Blender's functionality
import bpy

# extend Python's math functionality
import math


def hex_color_to_rgba(hex_color):
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


hex_color = "#FFD43B"
rgba_color = hex_color_to_rgba(hex_color)

# add a plane into the scene
bpy.ops.mesh.primitive_plane_add()

# create a new material
material = bpy.data.materials.new(name=f"hex_color_{hex_color}")
material.diffuse_color = rgba_color

# add material to object
bpy.context.active_object.data.materials.append(material)
