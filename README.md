# OpenFOAM-Blender Bridge v1.0

A professional-grade Blender add-on designed to automate the generation of OpenFOAM configuration files. This tool bridges the gap between 3D modeling and CFD simulation setup.

## Features
- **SimFlow-Style Workflow:** Sequential UI panels guide users from workspace setup to solver execution.
- **Data Validation:** Built-in clamping for physical parameters (e.g., Delta T) to prevent solver crashes.
- **Persistent Storage:** Simulation settings are saved directly within the Blender `.blend` file.

## How to Use
1. **Installation:** Install the provided `.zip` file via Blender Preferences.
2. **Access:** Open the 3D Viewport Sidebar (Press `N`) and select the **OpenFOAM** tab.
3. **Workspace Setup:** Define the absolute path for your OpenFOAM case directory.
4. **Configure Physics:** Select your solver (e.g., icoFoam) and set the simulation end time and time-steps.
5. **Generate:** Click **Generate controlDict**. The add-on creates the necessary directory structure and the `system/controlDict` file.

## Technical Architecture
For future developers:
- `properties.py`: Defines the `OpenFoamProperties` class using `bpy.props`.
- `ui.py`: Implements the `bpy.types.Panel` following SimFlow's hierarchical UI design.
- `operators.py`: Handles the OS-level file writing and string formatting.