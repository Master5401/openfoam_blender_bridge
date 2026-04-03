import bpy
import os


class OPENFOAM_OT_WriteConfig(bpy.types.Operator):
    bl_idname = "openfoam.write_config"
    bl_label = "Generate controlDict"

    def execute(self, context):
        props = context.scene.openfoam_props

        # The controlDict Content
        content = f"application {props.solver};\nstartTime 0;\nendTime {props.end_time};\ndeltaT {props.delta_t};\nwriteInterval {props.write_interval};"

        # Path Logic
        path = bpy.path.abspath(props.case_dir)
        sys_path = os.path.join(path, "system")

        if not os.path.exists(sys_path):
            os.makedirs(sys_path)

        with open(os.path.join(sys_path, "controlDict"), "w") as f:
            f.write(content)

        self.report({'INFO'}, f"File written to {sys_path}")
        return {'FINISHED'}