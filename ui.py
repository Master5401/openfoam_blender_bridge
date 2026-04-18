import bpy

class OPENFOAM_OT_SolverDialog(bpy.types.Operator):
    bl_idname = "openfoam.solver_dialog"
    bl_label = "OpenFOAM Solver Setup (Project 4)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=550)

    def draw(self, context):
        layout = self.layout
        props = context.scene.openfoam_props

        # Core Config
        box = layout.box()
        box.label(text="Case & Physics Configuration", icon='PHYSICS')
        box.prop(props, "case_dir")
        box.prop(props, "solver")
        box.prop(props, "turbulence")
        box.prop(props, "use_dynamic_mesh")

        # Time & Mesh
        col = box.column(align=True)
        col.prop(props, "end_time")
        col.prop(props, "delta_t")
        
        # Kinematics
        box = layout.box()
        box.label(text="Kinematic Boundaries (0/)", icon='GROUP_VERTEX')
        box.prop(props, "init_pressure")
        box.prop(props, "lid_velocity")
        
        # Turbulence Params (Dynamic rendering based on selection)
        if props.turbulence != 'laminar':
            box.label(text="Turbulence Variables:", icon='MOD_FLUIDSIM')
            if "k" in props.turbulence: box.prop(props, "turb_k")
            if props.turbulence == 'kEpsilon': box.prop(props, "turb_epsilon")
            if props.turbulence == 'kOmega': box.prop(props, "turb_omega")

        layout.separator()
        layout.label(text="Automated Pipeline Actions:", icon='CONSOLE')
        layout.operator("openfoam.write_config", icon='FILE_TICK')
        layout.operator("openfoam.write_blockmesh", icon='MOD_MESHDEFORM')
        layout.operator("openfoam.write_boundary", icon='GROUP_VERTEX')
        
        layout.separator()
        row = layout.row()
        row.scale_y = 1.5
        row.operator("openfoam.run_simulation", icon='PLAY')
        row.operator("openfoam.run_paraview", icon='RESTRICT_VIEW_OFF')

class OPENFOAM_PT_Launcher(bpy.types.Panel):
    bl_label = "CFD Engine"
    bl_idname = "OPENFOAM_PT_Launcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'OpenFOAM'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Project 4 MVP Engine")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("openfoam.solver_dialog", text="Launch Solver UI", icon='WINDOW')
