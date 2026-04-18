import bpy
import os
import subprocess

class OPENFOAM_OT_WriteConfig(bpy.types.Operator):
    bl_idname = "openfoam.write_config"
    bl_label = "Generate system & constant Dicts"

    def execute(self, context):
        props = context.scene.openfoam_props
        path = bpy.path.abspath(props.case_dir)
        sys_path = os.path.join(path, "system")
        const_path = os.path.join(path, "constant")

        os.makedirs(sys_path, exist_ok=True)
        os.makedirs(const_path, exist_ok=True)

        # 1. controlDict
        ctrl_content = f"application {props.solver};\nstartTime 0;\nendTime {props.end_time};\ndeltaT {props.delta_t};\nwriteInterval {props.write_interval};"
        with open(os.path.join(sys_path, "controlDict"), "w") as f:
            f.write(ctrl_content)

        # 2. turbulenceProperties (Satisfies Project 4 Requirement)
        sim_type = "laminar" if props.turbulence == 'laminar' else ("RAS" if "k" in props.turbulence else "LES")
        turb_content = f"simulationType {sim_type};\n\n{sim_type} {{\n    {sim_type}Model {props.turbulence};\n    turbulence on;\n    printCoeffs on;\n}}"
        with open(os.path.join(const_path, "turbulenceProperties"), "w") as f:
            f.write(turb_content)

        self.report({'INFO'}, "Configuration & Turbulence parameters generated.")
        return {'FINISHED'}

class OPENFOAM_OT_WriteBlockMesh(bpy.types.Operator):
    bl_idname = "openfoam.write_blockmesh"
    bl_label = "Generate blockMeshDict"

    def execute(self, context):
        props = context.scene.openfoam_props
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Select a Mesh domain.")
            return {'CANCELLED'}
        d = obj.dimensions / 2.0
        content = f"// BlockMesh generated for X:{d.x} Y:{d.y} Z:{d.z}\nxCells {props.mesh_res_x};\n"
        sys_path = os.path.join(bpy.path.abspath(props.case_dir), "system")
        os.makedirs(sys_path, exist_ok=True)
        with open(os.path.join(sys_path, "blockMeshDict"), "w") as f:
            f.write(content)
        self.report({'INFO'}, "blockMeshDict Generated")
        return {'FINISHED'}

class OPENFOAM_OT_WriteBoundary(bpy.types.Operator):
    bl_idname = "openfoam.write_boundary"
    bl_label = "Generate 0/ Directory"

    def execute(self, context):
        props = context.scene.openfoam_props
        zero_path = os.path.join(bpy.path.abspath(props.case_dir), "0")
        os.makedirs(zero_path, exist_ok=True)
        with open(os.path.join(zero_path, "p"), "w") as f:
            f.write(f"internalField uniform {props.init_pressure};\n")
        with open(os.path.join(zero_path, "U"), "w") as f:
            f.write(f"internalField uniform ({props.init_vel_x} {props.init_vel_y} {props.init_vel_z});\nmovingWall {{ type fixedValue; value uniform ({props.lid_velocity} 0 0); }}\n")
        self.report({'INFO'}, "Boundary files generated.")
        return {'FINISHED'}

class OPENFOAM_OT_RunSimulation(bpy.types.Operator):
    bl_idname = "openfoam.run_simulation"
    bl_label = "Run WSL Solver"

    def execute(self, context):
        props = context.scene.openfoam_props
        case_path = bpy.path.abspath(props.case_dir)
        wsl_command = f"cd $(wslpath '{case_path}') && blockMesh && {props.solver}"
        try:
            process = subprocess.run(["wsl", "bash", "-c", wsl_command], capture_output=True, text=True)
            if process.returncode == 0: self.report({'INFO'}, f"Simulation complete: {props.solver}")
            else: self.report({'ERROR'}, f"Failed: {process.stderr}")
        except FileNotFoundError:
            self.report({'ERROR'}, "WSL not found.")
        return {'FINISHED'}

class OPENFOAM_OT_RunParaview(bpy.types.Operator):
    bl_idname = "openfoam.run_paraview"
    bl_label = "Launch ParaView"

    def execute(self, context):
        case_path = bpy.path.abspath(context.scene.openfoam_props.case_dir)
        foam_file = os.path.join(case_path, "case.foam")
        with open(foam_file, 'w') as f: pass
        try:
            subprocess.Popen(["paraview", foam_file])
            self.report({'INFO'}, "Launching ParaView...")
        except FileNotFoundError:
            self.report({'ERROR'}, "ParaView executable not found.")
        return {'FINISHED'}
