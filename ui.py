import bpy

class OPENFOAM_PT_Sidebar(bpy.types.Panel):
    bl_label = "SimFlow Bridge"
    bl_idname = "OPENFOAM_PT_Sidebar"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'OpenFOAM'

    def draw(self, context):
        layout = self.layout
        props = context.scene.openfoam_props

        # Setup & Physics
        box = layout.box()
        box.label(text="Workflow: Setup", icon='PROPERTIES')
        box.prop(props, "case_dir")

        box = layout.box()
        box.label(text="Physics", icon='PHYSICS')
        box.prop(props, "solver")

        box = layout.box()
        box.label(text="Runtime", icon='TIME')
        box.prop(props, "end_time")
        box.prop(props, "delta_t")
        box.prop(props, "write_interval")

        layout.operator("openfoam.write_config", icon='FILE_TICK')
        
        box = layout.box()
        box.label(text="Mesh Generation", icon='MESH_CUBE')
        col = box.column(align=True)
        col.prop(props, "mesh_res_x")
        col.prop(props, "mesh_res_y")
        col.prop(props, "mesh_res_z")
        
        layout.separator()
        layout.operator("openfoam.write_blockmesh", text="Generate blockMeshDict", icon='MOD_MESHDEFORM')

        box = layout.box()
        box.label(text="Boundary Conditions (0/)", icon='GROUP_VERTEX')
        
        col = box.column(align=True)
        col.label(text="Initial Internal Field:")
        col.prop(props, "init_pressure")
        
        row = col.row(align=True)
        row.prop(props, "init_vel_x", text="U_x")
        row.prop(props, "init_vel_y", text="U_y")
        row.prop(props, "init_vel_z", text="U_z")
        
        layout.separator()
        
        col = box.column(align=True)
        col.label(text="Patch Setup (Cavity Demo):")
        col.prop(props, "lid_velocity")