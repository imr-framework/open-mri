# OpenMRI — Open MRI Design, Fabrication and Testing Format

OpenMRI is a **human‑readable, interoperable** file and folder standard for **open-source MRI scanner design, fabrication and testing**, with a focus on **low-field systems**. Think of it as doing for **MR scanner design** what **Pulseq** did for **sequence design**.

## Goals
- Portable designs across labs and vendors.
- Reproducible fabrication and assembly.
- Clear coordinate systems & units.
- Extensible to different magnet and coil geometries (Halbach, C-, H-type, cylindrical, planar).
- Validation & versioning baked in.

## Core concepts
- A repository (or zip) is an **OpenMRI package**.
- The package has a top-level manifest: `scanner.yaml`.
- All CAD/fieldmaps/BOM/test data live in subfolders and are referenced by relative paths with checksums.
- JSON Schema + Pydantic validate the manifest.
- Everything uses **SI units**, **right-handed RAS** scanner coordinates by default (configurable via transforms).

## Quick start (CLI)
```bash
python3 -m venv openmrd
source openmrd/bin/activate
pip install -e .
openmrd init my_scanner --template halbach_lowfield
openmrd validate my_scanner/scanner.yaml
```

## Status
This is a **v0.1** proposal meant to bootstrap community discussion. PRs welcome!

<div align="center">
  <img src="https://github.com/user-attachments/assets/d8a7c6e1-9337-4a7d-88c9-b72ed52cbec9" width="200">
</div>

 **Building: Repositories list** 
1.  Magnet: design and simulation
2.  Magnet: construction
3.  [Field mapping robot](https://github.com/imr-framework/mapping_robot)
4.  [Passive shimming including 3D STL file generation](https://github.com/imr-framework/passive_shimming)
5.  [Amplifiers: Gradient, RF TX and RF RX - 3rd party - Larry Wald/Martinos/MGH](https://tabletop.martinos.org/index.php?title=Main_Page)
6.  [Planar gradient coil design using pycoilgen](https://github.com/sairamgeethanath/pyCoilGen) and [previous effort](https://github.com/imr-framework/planar_gradient_coil_design/tree/main)
7.  RF coil: design and simulation
8.  RF coil: construction
9.  [Spectrometer - 3rd party - FLOCRA; part of console software download](https://github.com/vnegnev)
10. [Pulse sequence design using Pypulseq](https://github.com/imr-framework/pypulseq)
11. [Console software](https://github.com/sairamgeethanath/console)
12. Phantom 
13. Scanner log and outputs


 **Playing: Repositories list** 
 1. [Virtual Scanner Tabletop Games](https://github.com/imr-framework/vs-tabletop/tree/delta-diy)
 2. [Virtual Scanner](https://github.com/imr-framework/virtual-scanner/)

## Our image currently looks like ....
<img src="https://github.com/user-attachments/assets/423c93c2-c405-448e-8fd6-d84fc44a69a9" width="200">





## Potential student projects

***Hardware**
1.  Field mapping robot - Design covers, wiring and a user interface
2.  Passive shims - explore new geometries and new optimization methods
3.  RF coils - Bat head coil matching the anatomy of its head

***MR physics***
1. Pulse sequences - Robust RF frequency finder, refine calibration sequences - RF power, gradient  
2. Image reconstruction - Multiple k-space filters 

***Software***
1. Console - automate install and startup 
2. Interface virtual scanner games with the console using the Pulseq format

***New experiments***
1. T1 mapping
2. T2 mapping

**Acknowledgement**:
1. Johns Hopkins Provost DELTA award, 2024 
