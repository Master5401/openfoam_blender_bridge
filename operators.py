import bpy
import os
import subprocess

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content)

class OPENFOAM_OT_WriteConfig(bpy.types.Operator):
    bl_idname = "openfoam.write_config"
    bl_label = "Generate system & constant Dicts"

    def execute(self, context):
        props = context.scene.openfoam_props
        path = bpy.path.abspath(props.case_dir)
        os.makedirs(os.path.join(path, "system"), exist_ok=True)
        os.makedirs(os.path.join(path, "constant"), exist_ok=True)

        # 1. controlDict
        ctrl = f"FoamFile {{ version 2.0; format ascii; class dictionary; object controlDict; }}\napplication {props.solver};\nstartTime 0;\nendTime {props.end_time};\ndeltaT {props.delta_t};\nwriteInterval {props.write_interval};"
        write_file(os.path.join(path, "system", "controlDict"), ctrl)

        # 2. turbulenceProperties
        sim_type = "laminar" if props.turbulence == 'laminar' else ("RAS" if "k" in props.turbulence else "LES")
        turb = f"FoamFile {{ version 2.0; format ascii; class dictionary; object turbulenceProperties; }}\nsimulationType {sim_type};\n\n{sim_type} {{\n    {sim_type}Model {props.turbulence};\n    turbulence on;\n    printCoeffs on;\n}}"
        write_file(os.path.join(path, "constant", "turbulenceProperties"), turb)
        
        # 3. Dynamic Mesh (FOSSEE Requirement)
        if props.use_dynamic_mesh:
            dyn = f"FoamFile {{ version 2.0; format ascii; class dictionary; object dynamicMeshDict; }}\ndynamicFvMesh dynamicMotionSolverFvMesh;\nmotionSolverLibs ( \"libfvMotionSolvers.so\" );\nsolver displacementLaplacian;"
            write_file(os.path.join(path, "constant", "dynamicMeshDict"), dyn)

        self.report({'INFO'}, "Configuration generated.")
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
        content = f"FoamFile {{ version 2.0; format ascii; class dictionary; object blockMeshDict; }}\n// BlockMesh for X:{d.x} Y:{d.y} Z:{d.z}\nxCells {props.mesh_res_x};\n"
        sys_path = os.path.join(bpy.path.abspath(props.case_dir), "system")
        os.makedirs(sys_path, exist_ok=True)
        write_file(os.path.join(sys_path, "blockMeshDict"), content)
        self.report({'INFO'}, "blockMeshDict Generated")
        return {'FINISHED'}

class OPENFOAM_OT_WriteBoundary(bpy.types.Operator):
    bl_idname = "openfoam.write_boundary"
    bl_label = "Generate 0/ Directory"

    def execute(self, context):
        props = context.scene.openfoam_props
        zero_path = os.path.join(bpy.path.abspath(props.case_dir), "0")
        os.makedirs(zero_path, exist_ok=True)
        
        # Base Kinematics
        write_file(os.path.join(zero_path, "p"), f"FoamFile {{ version 2.0; format ascii; class volScalarField; object p; }}\ndimensions [0 2 -2 0 0 0 0];\ninternalField uniform {props.init_pressure};\nboundaryField {{ movingWall {{ type zeroGradient; }} fixedWalls {{ type zeroGradient; }} frontAndBack {{ type empty; }} }}")
        write_file(os.path.join(zero_path, "U"), f"FoamFile {{ version 2.0; format ascii; class volVectorField; object U; }}\ndimensions [0 1 -1 0 0 0 0];\ninternalField uniform (0 0 0);\nboundaryField {{ movingWall {{ type fixedValue; value uniform ({props.lid_velocity} 0 0); }} fixedWalls {{ type noSlip; }} frontAndBack {{ type empty; }} }}")
        
        # Safe Turbulence Initialization to prevent Fatal Error
        if props.turbulence != 'laminar':
            nut = f"FoamFile {{ version 2.0; format ascii; class volScalarField; object nut; }}\ndimensions [0 2 -1 0 0 0 0];\ninternalField uniform 0;\nboundaryField {{ movingWall {{ type nutkWallFunction; value uniform 0; }} fixedWalls {{ type nutkWallFunction; value uniform 0; }} frontAndBack {{ type empty; }} }}"
            write_file(os.path.join(zero_path, "nut"), nut)
            
            if "k" in props.turbulence:
                k = f"FoamFile {{ version 2.0; format ascii; class volScalarField; object k; }}\ndimensions [0 2 -2 0 0 0 0];\ninternalField uniform {props.turb_k};\nboundaryField {{ movingWall {{ type kqRWallFunction; value uniform {props.turb_k}; }} fixedWalls {{ type kqRWallFunction; value uniform {props.turb_k}; }} frontAndBack {{ type empty; }} }}"
                write_file(os.path.join(zero_path, "k"), k)
                
            if props.turbulence == 'kEpsilon':
                eps = f"FoamFile {{ version 2.0; format ascii; class volScalarField; object epsilon; }}\ndimensions [0 2 -3 0 0 0 0];\ninternalField uniform {props.turb_epsilon};\nboundaryField {{ movingWall {{ type epsilonWallFunction; value uniform {props.turb_epsilon}; }} fixedWalls {{ type epsilonWallFunction; value uniform {props.turb_epsilon}; }} frontAndBack {{ type empty; }} }}"
                write_file(os.path.join(zero_path, "epsilon"), eps)
                
            if props.turbulence == 'kOmega':
                omg = f"FoamFile {{ version 2.0; format ascii; class volScalarField; object omega; }}\ndimensions [0 0 -1 0 0 0 0];\ninternalField uniform {props.turb_omega};\nboundaryField {{ movingWall {{ type omegaWallFunction; value uniform {props.turb_omega}; }} fixedWalls {{ type omegaWallFunction; value uniform {props.turb_omega}; }} frontAndBack {{ type empty; }} }}"
                write_file(os.path.join(zero_path, "omega"), omg)

        self.report({'INFO'}, "Boundary condition dictionaries safely generated.")
        return {'FINISHED'}

class OPENFOAM_OT_RunSimulation(bpy.types.Operator):
    bl_idname = "openfoam.run_simulation"
    bl_label = "Run WSL Solver"

    def execute(self, context):
        props = context.scene.openfoam_props
        case_path = bpy.path.abspath(props.case_dir)
        
        # Execute WSL Bridge
        wsl_command = f"cd $(wslpath '{case_path}') && blockMesh && {props.solver}"
        try:
            process = subprocess.run(["wsl", "bash", "-ic", wsl_command], capture_output=True, text=True)
            if process.returncode == 0: 
                self.report({'INFO'}, f"Simulation complete: {props.solver}")
            else: 
                self.report({'ERROR'}, f"Failed: {process.stderr}")
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
        except FileNotFoundError:
            self.report({'ERROR'}, "ParaView executable not found.")
        return {'FINISHED'}
