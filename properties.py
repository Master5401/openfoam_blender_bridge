import bpy

class OpenFoamProperties(bpy.types.PropertyGroup):
    case_dir: bpy.props.StringProperty(name="Case Path", subtype='DIR_PATH')
    solver: bpy.props.EnumProperty(
        name="Solver",
        items=[('icoFoam', "icoFoam (Laminar)", ""), ('simpleFoam', "simpleFoam (Steady)", "")]
    )
    turbulence: bpy.props.EnumProperty(
        name="Turbulence Model",
        items=[
            ('laminar', "Laminar", ""),
            ('kEpsilon', "RANS: k-Epsilon", ""),
            ('kOmega', "RANS: k-Omega", ""),
            ('Smagorinsky', "LES: Smagorinsky", "")
        ]
    )
    end_time: bpy.props.FloatProperty(name="End Time", default=10.0, min=0.1)
    delta_t: bpy.props.FloatProperty(name="Delta T", default=0.005, min=0.0001, precision=4)
    write_interval: bpy.props.IntProperty(name="Write Interval", default=20, min=1)
    
    mesh_res_x: bpy.props.IntProperty(name="X Cells", default=15, min=1)
    mesh_res_y: bpy.props.IntProperty(name="Y Cells", default=15, min=1)
    mesh_res_z: bpy.props.IntProperty(name="Z Cells", default=15, min=1)

    init_pressure: bpy.props.FloatProperty(name="Internal Pressure (p)", default=0.0)
    init_vel_x: bpy.props.FloatProperty(name="Internal U_x", default=0.0)
    init_vel_y: bpy.props.FloatProperty(name="Internal U_y", default=0.0)
    init_vel_z: bpy.props.FloatProperty(name="Internal U_z", default=0.0)
    lid_velocity: bpy.props.FloatProperty(name="Moving Wall Velocity", default=1.0)
