import bpy
from . import properties, operators, ui

bl_info = {
    "name": "OpenFOAM Blender Bridge",
    "author": "Shakunth Srinivasan",
    "version": (1, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > OpenFOAM",
    "category": "Add-on",
}

classes = (
    properties.OpenFoamProperties,
    operators.OPENFOAM_OT_WriteConfig,
    operators.OPENFOAM_OT_WriteBlockMesh,
    operators.OPENFOAM_OT_WriteBoundary,
    operators.OPENFOAM_OT_RunSimulation,
    operators.OPENFOAM_OT_RunParaview,
    ui.OPENFOAM_OT_SolverDialog,
    ui.OPENFOAM_PT_Launcher
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.openfoam_props = bpy.props.PointerProperty(type=properties.OpenFoamProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.openfoam_props
