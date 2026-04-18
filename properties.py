import bpy

class OpenFoamProperties(bpy.types.PropertyGroup):
    case_dir: bpy.props.StringProperty(name="Case Path", subtype='DIR_PATH')
    
    solver: bpy.props.EnumProperty(
        name="Solver",
        items=[('icoFoam', "icoFoam (Laminar)", ""), ('pisoFoam', "pisoFoam (LES/RANS)", ""), ('simpleFoam', "simpleFoam (Steady)", "")]
    )
    
    turbulence: bpy.props.EnumProperty(
        name="Turbulence",
        items=[
            ('laminar', "Laminar", ""),
            ('kEpsilon', "RANS: k-Epsilon", ""),
            ('kOmega', "RANS: k-Omega", ""),
            ('Smagorinsky', "LES: Smagorinsky", "")
        ]
    )
    
    use_dynamic_mesh: bpy.props.BoolProperty(name="Enable Dynamic Mesh", default=False)
    
    end_time: bpy.props.FloatProperty(name="End Time", default=0.5, min=0.001)
    delta_t: bpy.props.FloatProperty(name="Delta T", default=0.001, min=0.00001, precision=5)
    write_interval: bpy.props.IntProperty(name="Write Interval", default=20, min=1)
    
    mesh_res_x: bpy.props.IntProperty(name="X Cells", default=20, min=1)
    mesh_res_y: bpy.props.IntProperty(name="Y Cells", default=20, min=1)
    mesh_res_z: bpy.props.IntProperty(name="Z Cells", default=1, min=1)

    init_pressure: bpy.props.FloatProperty(name="Internal Pressure (p)", default=0.0)
    lid_velocity: bpy.props.FloatProperty(name="Wall Velocity (U_x)", default=1.0)
    
    # Turbulence Initial Conditions
    turb_k: bpy.props.FloatProperty(name="Init k", default=0.00375, precision=5)
    turb_epsilon: bpy.props.FloatProperty(name="Init epsilon", default=0.011, precision=5)
    turb_omega: bpy.props.FloatProperty(name="Init omega", default=2.93, precision=5)
