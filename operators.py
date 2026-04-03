import bpy
import os


class OPENFOAM_OT_WriteConfig(bpy.types.Operator):
    bl_idname = "openfoam.write_config"
    bl_label = "Generate controlDict"

    def execute(self, context):
        props = context.scene.openfoam_props

        content = f"application {props.solver};\nstartTime 0;\nendTime {props.end_time};\ndeltaT {props.delta_t};\nwriteInterval {props.write_interval};"

        path = bpy.path.abspath(props.case_dir)
        sys_path = os.path.join(path, "system")

        if not os.path.exists(sys_path):
            os.makedirs(sys_path)

        with open(os.path.join(sys_path, "controlDict"), "w") as f:
            f.write(content)

        self.report({'INFO'}, f"File written to {sys_path}")
        return {'FINISHED'}


class OPENFOAM_OT_WriteBlockMesh(bpy.types.Operator):
    bl_idname = "openfoam.write_blockmesh"
    bl_label = "Generate blockMeshDict"

    def execute(self, context):
        props = context.scene.openfoam_props
        obj = context.active_object

        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a Mesh domain in the 3D viewport")
            return {'CANCELLED'}

        d = obj.dimensions / 2.0
        l, w, h = d.x, d.y, d.z

        verts = f"""
vertices
(
    ({-l} {-w} {-h}) ({l} {-w} {-h}) ({l} {w} {-h}) ({-l} {w} {-h})
    ({-l} {-w} {h}) ({l} {-w} {h}) ({l} {w} {h}) ({-l} {w} {h})
);"""

        blocks = f"""
blocks
(
    hex (0 1 2 3 4 5 6 7) ({props.mesh_res_x} {props.mesh_res_y} {props.mesh_res_z}) simpleGrading (1 1 1)
);"""

        content = f"FoamFile\n{{\n    version     2.0;\n    format      ascii;\n    class       dictionary;\n    object      blockMeshDict;\n}}\n\nconvertToMeters 1;\n{verts}\n{blocks}\n\nedges ();\nboundary ();\nmergePatchPairs ();\n"

        sys_path = os.path.join(bpy.path.abspath(props.case_dir), "system")
        if not os.path.exists(sys_path):
            os.makedirs(sys_path)

        with open(os.path.join(sys_path, "blockMeshDict"), "w") as f:
            f.write(content)

        self.report({'INFO'}, "blockMeshDict Generated Successfully")
        return {'FINISHED'}