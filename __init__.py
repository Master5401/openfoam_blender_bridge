import bpy
from . import properties, operators, ui

bl_info = {
    "name": "OpenFOAM Blender Bridge",
    "author": "Shakunth Srinivasan",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > OpenFOAM",
    "category": "Add-on",
}

def register():
    bpy.utils.register_class(properties.OpenFoamProperties)
    bpy.types.Scene.openfoam_props = bpy.props.PointerProperty(type=properties.OpenFoamProperties)
    bpy.utils.register_class(operators.OPENFOAM_OT_WriteConfig)
    bpy.utils.register_class(ui.OPENFOAM_PT_Sidebar)

def unregister():
    bpy.utils.unregister_class(properties.OpenFoamProperties)
    bpy.utils.unregister_class(operators.OPENFOAM_OT_WriteConfig)
    bpy.utils.unregister_class(ui.OPENFOAM_PT_Sidebar)