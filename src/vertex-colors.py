import bpy


for o in bpy.context.selected_objects:

    if o.type != 'MESH':

        continue

    if len(o.data.vertex_colors) != 0:

        continue


    o.data.vertex_colors.new()